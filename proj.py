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

def main(arg):
    dataset = importDataFromCSV(arg)
    train, test = splitTrainingTesting(dataset)
    print ("Set Sizes: ")
    print ("Training set: " + str(len(train)) + " | Testing Set: " + str(len(test)) + " | Data set: " + str(len(dataset)))
    # print ("Data set: ")
    # for row in dataset:
    #     print (row)
    # print ("Training set: ")
    # for row in train:
    #     print (row)
    # print ("Testing set: ")
    # for row in test:
    #     print (row)
    
main(sys.argv[1])