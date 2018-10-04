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
def isValidChromosome(chromosome) :
    if sumCost(chromosome) > crowdfund_amount :
        return False
    return True
'''
test_chromo = [0, 23, 0, 0, 5]
print isValidChromosome(test_chromo)
'''
randomAwardThreshold = float(70/100)
# handles interest constraint
def generateChromosome() :
    chromosome = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    while True :
        for i in range(0, noOfApplicants) :
            randomChoice = random.uniform(0,1)
            if randomChoice > randomAwardThreshold :
                choiceConf = random.randint(0, len(trackWiseConf[applicantValues[i][4]-1])-1)
                chromosome[i] = trackWiseConf[applicantValues[i][4]-1][choiceConf]
        if isValidChromosome(chromosome) :
            break   
    return chromosome
print generateInitialPopulation()


