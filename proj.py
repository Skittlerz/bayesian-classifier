#
#   CS 421 Project - Naive Bayes implementation
#
#   To Run:
#     `python3 proj.py filename_of_csv_dataset`
#

import sys
import csv
import random
# from statistics import mean
# from statistics import stdev
# from scipy.stats import norm

### USEFUL UTILITY FUNCTIONS ###

def importDataFromCSV(filename):
    data = []
    with open(filename, newline = '') as file:
        raw_data = csv.reader(file, delimiter = ',')
        try: 
            for row in raw_data:
                data.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return data

def splitTrainingTesting(dataset):
    size_train = int(len(dataset) * 0.70) # TODO find appropriate split ratio
    train = []
    test = dataset[:]
    while len(train) < size_train:
        train.append(test.pop(random.randrange(len(test))))
    return train, test

def splitByCol(dataset, colIndex):
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
    # print ("Split the dataset into a dictionary of attribute: [members with that attribute]")
    # print (split)
    # print (norm(73, 6.2).pdf(71.5)) # norm(mean, stdev).pdf(x)
    
    
main(sys.argv[1])