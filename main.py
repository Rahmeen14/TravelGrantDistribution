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

# Creating a list of lists 
trackWiseConf = [[]] * len(trackValues)

for i in range(0, len(confValues)) :
    index = tracks_map[str(confValues[i][1])]
    print index
    if len(trackWiseConf[index-1]) ==  0:
        trackWiseConf[index-1] = []
    trackWiseConf[index-1].append(i)