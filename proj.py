#
#   CS 421 Project - Naive Bayes implementation
#
#   To Run:
#     `python proj.py filename_of_csv_dataset`
#   Dependencies:
#     statistics, scipy
#     `pip install statistics` 
#     `pip install scipy`      
#

import sys
import csv
import random
# from statistics import mean
# from statistics import stdev
# from scipy.stats import norm

### USEFUL UTILITY FUNCTIONS ###

# Takes data from `filename` and returns a data object
def importDataFromCSV(filename):
    data = []
    with open(filename) as file:
        raw_data = csv.reader(file, delimiter = ',')
        try: 
            for row in raw_data:
                data.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return data

# Takes dataset and returns a training set and a testing set split by splitRatio
# For default splitRatio (0.70), a random 70% of the data will be in the training 
# set and the remaining 30% will be in the testing set
def splitTrainingTesting(dataset, splitRatio = 0.70):
    assert (splitRatio < 1.00 and splitRatio > 0.00)
    size_train = int(len(dataset) * splitRatio)
    train = []
    test = dataset[:]
    while len(train) < size_train:
        train.append(test.pop(random.randrange(len(test))))
    return train, test

# Splits a data set into a dictionary of the form:
# `attribute: [members with that attribute]`
# where attribute is given by the colIndex (default last item)
def splitByCol(dataset, colIndex = -1):
    split = {}
    for i in range(len(dataset)):
        row = dataset[i]
        if row[colIndex] not in split:
            split[row[colIndex]] = []
        split[row[colIndex]].append(row)
    return split

def main(arg):
    dataset = importDataFromCSV(arg)
    train, test = splitTrainingTesting(dataset)
    # print ("Set Sizes: ")
    # print ("Training set: " + str(len(train)) + " | Testing Set: " + str(len(test)) + " | Data set: " + str(len(dataset)))
    # print ("Data set: ")
    # for row in dataset:
    #     print (row)
    # print ("Training set: ")
    # for row in train:
    #     print (row)
    # print ("Testing set: ")
    # for row in test:
    #     print (row)
    # split = splitByCol(train, 6) # 6 is the index of religion in the dataset
    # print ("Split the dataset into a dictionary of `attribute: [members with that attribute]`")
    # print (split)
    # print (norm(73, 6.2).pdf(71.5)) # norm(mean, stdev).pdf(x)
    
main(sys.argv[1])