#
#   CS 421 Project - Naive Bayes implementation
#

import csv
from random import randint
from time import process_time

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
    assert (0.00 < splitRatio < 1.00)
    size_train = int(len(dataset) * splitRatio)
    train = []
    test = dataset[:]
    while len(train) < size_train:
        train.append(test.pop(randint(0, len(test) - 1)))
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

# Calculates the discrete probability of x appearing in collection
# Returns the value as a float
def calculateProbability(x, collection):
    if collection.count(x) > 0:
        return float(collection.count(x)) / len(collection)
    else:
        return 0.0000000001

# Creates a dictionary of the form:
# `attribute: probability for that attribute given the row data`
# using the probabilities given by the columns in the training dataset
def calculateAllProbabilities(row, train, target_attr = -1):
    probs = {}
    split = splitByCol(train, target_attr)
    for attr in split:
        if len(split[attr]) is 0:
            probs[attr] = 0
            continue
        col = [train_row[target_attr] for train_row in train]
        probs[attr] = calculateProbability(attr, col)
        for i in range(len(split[attr][0])):
            if i == target_attr:
                continue
            col = [train_row[i] for train_row in split[attr]]
            probs[attr] *= calculateProbability(row[i], col)
    return probs

# Comes up with a predicted target value based on the data in the training dataset
def predict(row, train, target_attr = -1):
    probabilities = calculateAllProbabilities(row, train, target_attr)
    high_attr, high_prob = None, -1.0
    for attr, prob in probabilities.items():
        if prob > high_prob:
            high_prob = prob
            high_attr = attr
    return high_attr

# Gets all of the predictions for each value in the test dataset
def getPredictions(train, test, target_attr = -1):
    predictions = []
    for row in test:
        predictions.append(predict(row, train, target_attr))
    return predictions

# For testing purposes; gets a random prediction from the domain for each value in the test dataset
def getRandomPredictions(test, domain):
    predictions = []
    for row in test:
        predictions.append(domain[randint(0, len(domain) - 1)])
    return predictions

# Gets the accuracy of the predictions as a percentage
def getAccuracy(test, predictions, target_attr = -1):
    correct = 0.0
    for i in range(len(test)):
        if test[i][target_attr] == predictions[i]:
            correct += 1.0
    return (correct / len(test)) * 100.0

# test
def test():
    dataset = importDataFromCSV("datasets/test.csv")
    assert (dataset)
    train, test = splitTrainingTesting(dataset)
    assert (train and test and len(train) == 7 and len(test) == 3)
    split = splitByCol(dataset)
    assert (split and len(split) == 7)
    prob = calculateProbability("2", dataset[0])
    assert (prob and prob == 0.4)
    probs = calculateAllProbabilities(dataset[0], dataset)
    assert (probs and len(probs) == 7)
    pred = predict(dataset[0], dataset)
    assert (pred and pred == "3")
    preds = getPredictions(dataset, dataset)
    assert (preds and preds == ["3", "2", "7", "2", "7", "8", "4", "3", "0", "1"])
    rand_preds = getRandomPredictions(dataset, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    assert (rand_preds)
    ac = getAccuracy(dataset, preds)
    assert (ac and ac == 100.0)

# main
def main():
    dataset = importDataFromCSV("datasets/flags/flag.data")
    num_trials = 100
    target = 6
    max_ac = 0
    min_ac = 100
    avg_ac = 0
    rand_max_ac = 0
    rand_min_ac = 100
    rand_avg_ac = 0
    start = process_time()
    for i in range(num_trials):
        train, test = splitTrainingTesting(dataset)
        predictions = getPredictions(train, test, target)
        accuracy = getAccuracy(test, predictions, target)
        avg_ac += accuracy / num_trials
        if max_ac < accuracy:
            max_ac = accuracy
        if min_ac > accuracy:
            min_ac = accuracy
    end = process_time()
    print ("Bayes Accuracy Average: " + str(round(avg_ac, 4)) + "%")
    print ("Bayes Accuracy Maximum: " + str(round(max_ac, 4)) + "%")
    print ("Bayes Accuracy Minimum: " + str(round(min_ac, 4)) + "%")
    print ("Bayes Accuracy Time: " + str(round(end - start, 4)) + " seconds")
    col = [row[target] for row in dataset]
    domain = list(set(col))
    rand_start = process_time()
    for i in range(num_trials):
        train, test = splitTrainingTesting(dataset)
        rand_predictions = getRandomPredictions(test, domain)
        rand_accuracy = getAccuracy(test, rand_predictions, target)
        rand_avg_ac += rand_accuracy / num_trials
        if rand_max_ac < rand_accuracy:
            rand_max_ac = rand_accuracy
        if rand_min_ac > rand_accuracy:
            rand_min_ac = rand_accuracy
    rand_end = process_time()
    print ("Random Accuracy Average: " + str(round(rand_avg_ac, 4)) + "%")
    print ("Random Accuracy Maximum: " + str(round(rand_max_ac, 4)) + "%")
    print ("Random Accuracy Minimum: " + str(round(rand_min_ac, 4)) + "%")
    print ("Random Accuracy Time: " + str(round(rand_end - rand_start, 4)) + " seconds")

test() 
main() 