from __future__ import division
import csv
import pandas 
import numpy
import random

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
        print randomChoice
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
    return float((50*(normalisedTotalPrestige) + 60*(normalisedTotalMerit) + 40*(normalisedTotalNoOfAwards))/(1 + 20*(normalisedCost) + 90*(normalisedTotalEconomicFitness)))

population = generateInitialPopulation()
print sumList
for i in range(0, POPULATION_SIZE):
   print fitnessOfChromosome(population[i])
