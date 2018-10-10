from __future__ import division
import csv
import pandas
import numpy
import random
import copy

POPULATION_SIZE = 20

crowdfund_amount = input("Enter the amount raised by crowdfunding")

# Extracting data from tracks database
conf_tracks = pandas.read_csv('data/tracks.csv')
ct_dataset = conf_tracks[0:]
trackValues = ct_dataset[0:].values.tolist()
tracks_map = {}
for i in range(0, len(trackValues)) :
    tracks_map[trackValues[i][1]] = int(trackValues[i][0])

# Extracting data from conferences database
conf_details = pandas.read_csv('data/conf_scholarships.csv')
cd_dataset = conf_details[0:]
confValues = cd_dataset[0:].values.tolist()

# Extracting data from applicants database
applicant_details = pandas.read_csv('data/applicant.csv')
ad_dataset = applicant_details[0:]
applicantValues = ad_dataset[0:].values.tolist()
noOfApplicants = len(applicantValues)

# Creating a list of lists, track wise for constraint management
trackWiseConf = [[]] * len(trackValues)

for i in range(0, len(confValues)) :
    index = tracks_map[str(confValues[i][1])]
    if len(trackWiseConf[index-1]) ==  0:
        trackWiseConf[index-1] = []
    trackWiseConf[index-1].append(i)


def generateInitialPopulation() :
    i = 0
    population = []
    while i != POPULATION_SIZE :
        chromosome = generateChromosome()
        while isValidChromosome(chromosome) != True :
            chromosome = generateChromosome()
        i = i + 1
        population.append(chromosome)
    return population


def sumCost(chromosome):
    sum = 0
    for j in range(0, 50):
        sum = sum + confValues[chromosome[j]-1][5]
    return sum


# handles cost constraint
sumList = []
def isValidChromosome(chromosome) :
    if sumCost(chromosome) > crowdfund_amount :
        return False
    sumList.append(sumCost(chromosome))
    return True
'''
test_chromo = [0, 23, 0, 0, 5]
print isValidChromosome(test_chromo)
'''


# handles interest constraint
def generateChromosome() :
    chromosome = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0, noOfApplicants) :
        randomChoice = random.randint(0,1)
        #print randomChoice
        if randomChoice == 1 :
            choiceConf = random.randint(0, len(trackWiseConf[applicantValues[i][4]-1])-1)
            chromosome[i] = trackWiseConf[applicantValues[i][4]-1][choiceConf]
    return chromosome

def sigmoid(x, derivative=False):
  return x*(1-x) if derivative else 1/(1+numpy.exp(-x))

def fitnessOfChromosome(chromosome) :
    totalNoOfAwards = 0

    totalPrestige = 0
    totalMerit = 0
    meritSum = 0
    ecoFitSum = 0
    totalEconomicFitness = 0
    normalisedCost = (sumCost(chromosome)/crowdfund_amount)
    for i in range(0, noOfApplicants) :
        if chromosome[i] == 0:
            continue
        else :
            totalNoOfAwards = totalNoOfAwards + 1
            totalPrestige = totalPrestige + confValues[chromosome[i]-1][4]
            totalMerit = totalMerit + applicantValues[i][3]
            totalEconomicFitness = totalEconomicFitness + applicantValues[i][2]
        meritSum = meritSum + applicantValues[i][3]
        ecoFitSum = ecoFitSum + applicantValues[i][2]
    normalisedTotalPrestige = (totalNoOfAwards/totalPrestige)
    normalisedTotalNoOfAwards = (totalNoOfAwards/noOfApplicants)
    normalisedTotalMerit = (totalMerit/meritSum)
    normalisedTotalEconomicFitness = (totalEconomicFitness/ecoFitSum) 
   
    #return float((sigmoid(normalisedTotalPrestige) + sigmoid(normalisedTotalMerit) + sigmoid(normalisedTotalNoOfAwards))/(1 + sigmoid(normalisedCost) + sigmoid(normalisedTotalEconomicFitness)))
    return float(((totalPrestige) + (totalMerit) + (totalNoOfAwards)+ (sumCost(chromosome)))/(1 + (totalEconomicFitness)))

def generatePopulationFitness(population) :
    population_fitness_dictionary = []
    for i in range(0, POPULATION_SIZE) :
        population_fitness_dictionary.append(fitnessOfChromosome(population[i]))
    return population_fitness_dictionary

def get_probability_list(population):
    fitness = generatePopulationFitness(population)
    total_fit = float(sum(fitness))
    relative_fitness = [f/total_fit for f in fitness]
    probabilities = [sum(relative_fitness[:i+1]) 
                     for i in range(len(relative_fitness))]
    return probabilities

def roulette_wheel_pop(population, probabilities, numberOfElite):
    chosen = []
    for n in xrange(numberOfElite):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probabilities[i]:
                chosen.append(list(individual))
                break
    return chosen

def alleleWiseCrossover(val1, val2) :
    st1 = list(str(val1))
    st2 = list(str(val2))
    c = st1[len(st1) - 1]
    st1[len(st1) - 1] = st2[len(st2) - 1]
    st2[len(st2) - 1] = c
    sT1 = ''.join(st1)
    sT2 = ''.join(st2)
    v1 = int(sT1)
    v2 = int(sT2)
    '''
    print type(v1)
    print v1
    print v2
    '''
    
    return val2, val1

def crossover(mating_pool) :
    temp_1 = random.randint(0, len(mating_pool)-1)
    temp_2 = random.randint(0, len(mating_pool)-1)    
    
    parent_copy_1 = copy.deepcopy(mating_pool[temp_1])
    parent_copy_2 = copy.deepcopy(mating_pool[temp_2])
    
    pivot_random = random.randint(0, noOfApplicants-1)
    for i in range(0, pivot_random) :
        #print mating_pool[temp_1]
        mating_pool[temp_1][i], mating_pool[temp_2][i] = alleleWiseCrossover(mating_pool[temp_1][i], mating_pool[temp_2][i])
    for i in range(pivot_random, noOfApplicants) :
        #print mating_pool[temp_2]
        mating_pool[temp_2][i], mating_pool[temp_1][i] = alleleWiseCrossover(mating_pool[temp_2][i], mating_pool[temp_1][i])
    
    return mating_pool
def printResult(fittest_chromosome) :
    for i in range(0, noOfApplicants) :
        if fittest_chromosome[i] != 0 :
            print applicantValues[i][1] + " : merit % = " + str(applicantValues[i][3]) + " and economic % = " + str(applicantValues[i][2]) + " interest = "+ str(applicantValues[i][4])
            print "Scholarship = " + str(confValues[fittest_chromosome[i] - 1][3]) + " rank = " + str(confValues[fittest_chromosome[i]-1][4]) + " subject = " + str(tracks_map[confValues[fittest_chromosome[i]-1][1]])
            print ""
    print ""
    print "Total money "+str(sumCost(fittest_chromosome))

def run_ga():
    
    population = generateInitialPopulation()

    for i in range(10):
        fitness_list = []
        avg_fitness = 0
        for member in population:
            mem_fitness = fitnessOfChromosome(member)
            fitness_list.append(mem_fitness)
            avg_fitness = avg_fitness + mem_fitness
        avg_fitness = avg_fitness/POPULATION_SIZE
        mating_pool = roulette_wheel_pop(population, get_probability_list(population), 20)
        population = crossover(mating_pool)
    fitness_of_population = []
    for i in range(0, POPULATION_SIZE):
        fitness_of_population.append(fitnessOfChromosome(population[i]))
    printResult(population[fitness_of_population.index(max(fitness_of_population))])
    
run_ga()
'''
population = generateInitialPopulation()
print roulette_wheel_pop(population, get_probability_list(population), POPULATION_SIZE)
'''

#mat_pool = [[0, 0, 97, 15, 0, 39, 0, 0, 76, 19, 0, 8, 65, 128, 0, 0, 29, 0, 56, 0, 126, 0, 18, 144, 142, 0, 0, 28, 0, 0, 113, 0, 0, 0, 0, 65, 0, 147, 86, 0, 70, 0, 128, 13, 0, 0, 8, 0, 0, 143], [59, 0, 0, 66, 0, 0, 37, 0, 0, 0, 64, 0, 0, 0, 70, 22, 0, 0, 60, 0, 8, 67, 0, 96, 0, 143, 0, 0, 0, 80, 0, 0, 1, 0, 0, 0, 0, 145, 0, 0, 0, 39, 65, 123, 0, 48, 0, 0, 0, 94]]

#crossover(mat_pool)
#alleleWiseCrossover(119, 67)
