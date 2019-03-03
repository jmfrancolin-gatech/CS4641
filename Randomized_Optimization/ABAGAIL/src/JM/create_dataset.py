import os
import csv
from collections import Counter

MAX_WORDS = 300

def make_dictionary(path):

    files = os.listdir(path)
    tweeter_feed_list = [path + tweeter_feed for tweeter_feed in files]
    words = []

    for tweeter_feed in tweeter_feed_list:
        f = open(tweeter_feed)
        blob = f.read()
        words += blob.split(" ")

    for i in range(len(words)):
        words[i] = words[i].lower()
        if not words[i].isalpha():
            words[i] = ""

    dictionary = Counter(words)
    del dictionary[""]

    return dictionary.most_common(MAX_WORDS)

def vectorize(path):

    files = os.listdir(path)
    tweeter_feed_list = [path + tweeter_feed for tweeter_feed in files]

    dataSet = []

    for tweeter_feed in tweeter_feed_list:
        data = []
        f = open(tweeter_feed)
        words = f.read().split(" ")
        for entry in dictionary:
            # entry[0] -> key // entry[1] -> value
            data.append((float)(words.count(entry[0])) / MAX_WORDS)

        # label = 'dem -> 0' || 'rep -> 1'
        if "dem" in tweeter_feed:
            data.append('dem')
        elif "rep" in tweeter_feed:
            data.append('rep')

        dataSet.append(data)

    return dataSet

### Main #######################################################################

"""Output Dataset for Political Affiliation Classification """

# declare input path
path = "tweets/"

# make dictionary from tweets
dictionary = make_dictionary(path)

# vectorize dictonary
dataSet = vectorize(path)

# output dataSet to csv file
dataSet_cvs = open("dataSet.csv",'w')
wr = csv.writer(dataSet_cvs, delimiter=",")
for i in range(len(dataSet)):
    wr.writerows([dataSet[i]])