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
import math
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
# where attribute is given by the targetClassCol (default last item)
def splitByCol(dataset, targetClassCol = -1):
    split = {}
    for i in range(len(dataset)):
        row = dataset[i]
        if row[targetClassCol] not in split:
            split[row[targetClassCol]] = []
        split[row[targetClassCol]].append(row)
    return split

 # Returns simple mean: sum of elements / num of elements
def mean(numbers):
    sum = 0
    for num in numbers:
        #could have null values
        if num:
            sum += float(num)
    return sum/float(len(numbers))

 # Returns standard deviation for N values: sqr root[ sum((x - mean)^2) / N - 1 ]
def standardDeviation(numbers):
    avg = mean(numbers)
    sum = 0
    for num in numbers:
        if num:
            sum += pow(float(num)-avg,2)
    variance = sum / float(len(numbers)-1)
    return math.sqrt(variance)

 # Returns array of [mean, standard deviation] for each attribute (column in the dataset)
def summarize(dataset, targetClassCol):
    summaries = [(mean(attribute), standardDeviation(attribute)) for attribute in zip(*dataset)]
	#remove column to be predicted
    del summaries[targetClassCol]
    return summaries

 # Group data rows by class value and summarize (compute mean, st dev)
def summarizeByClass(dataset, targetClassCol):
    separated = splitByCol(dataset, targetClassCol)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances, targetClassCol)
    return summaries

"""
Prediction Data Flow:
getPredictions  --> predict --> calculateClassProbabilities --> calculateProbability
"""

 # Probability density function
def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(float(x)-float(mean),2)/(2*math.pow(float(stdev),2))))
    return (1/(math.sqrt(2*math.pi)*stdev))*exponent

def calculateProbabilityDiscrete(x, inputVector):
    return float(inputVector.count(x)) / len(inputVector)

def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities

def calculateClassProbabilitiesDiscrete(inputVector):
    probabilities = {}
    for value in set(inputVector):
        if value in probabilities:
            probabilities[value] *= calculateProbabilityDiscrete(value, inputVector)
        else:
            probabilities[value] = calculateProbabilityDiscrete(value, inputVector)
    return probabilities

def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    #initialize with default values
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel

def predictDiscrete(inputVector):
    probabilities = calculateClassProbabilitiesDiscrete(inputVector)
    #initialize with default values
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel


def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions

def getPredictionsDiscrete(testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predictDiscrete(testSet[i])
        predictions.append(result)
    return predictions

def getAccuracy(testSet, predictions, targetClassCol):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][targetClassCol] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet)))*100.0

def main(arg):
    dataset = importDataFromCSV(arg)
    train, test = splitTrainingTesting(dataset)
    print('Split {0} rows into train = {1} and test = {2} rows'.format(len(dataset),len(train),len(test)))
    # print(train)
    #prepare model
    targetClassCol = 5
    #this will work sometimes - depends on what random data is pulled for the test set
    #otherwise program halts because of a divide-by-zero error
    #from what I can deduce it is the columns that are filled with [0,1] as possible values that are causing the issue
    # summaries = summarizeByClass(train, targetClassCol)
    # print(summaries)

    #test model
    predictions = getPredictionsDiscrete(test)
    accuracy = getAccuracy(test, predictions, targetClassCol)
    print('Accuracy: {0}%'.format(accuracy))

    # print ("Set Sizes: ")
    # print ("Training set: " + str(len(train)) + " | Testing Set: " + str(len(test)) + " | Data set: " + str(len(dataset)))
    # print ("Data set: ")
    # for row in dataset:
    #     print (row)
    #print ("Training set: ")
    #for row in train:
    #    print (row)
    #print ("Testing set: ")
    #for row in test:
    #    print (row)
    # split = splitByCol(train, 6) # 6 is the index of religion in the dataset
    # print ("Split the dataset into a dictionary of `attribute: [members with that attribute]`")
    # print (split)
    # print (norm(73, 6.2).pdf(71.5)) # norm(mean, stdev).pdf(x)
    
#main(sys.arg[1])

#temporary - just so I can run this from debugger in VS
#flagCopy has string values removed
filename = "datasets/flags/flagCopy.data"
main(filename)