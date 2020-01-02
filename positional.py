from extractor import Extractor
import os
from os import listdir
from os.path import isfile, join
import re
import json

PATH = "C:/Users/Sneha/Desktop/python/documents"

def getFiles():
    onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    return onlyfiles


def getKeywords():
    keyList = set()
    fileList = getFiles()

    for file in fileList:
        e = Extractor(open(PATH + "/" + file).read())
        keyList |= set(e.rank_words())

    return keyList    

def positionalIndex():
    position = {}
    fileList = getFiles()
    words = getKeywords()
    for word in words:
        location = position.setdefault(word, [])
        postingList = {}
        for file in fileList:
            if word in (open(PATH + "/" + file).read()).lower():
                pos = postingList.setdefault(file, [])
                index = []
                index = getPosition(word, PATH + "/" + file)
                pos.append(index)
        location.append(postingList)
    return position


def getPosition(word, filename):
    index = []
    text = open(filename).read().lower()
    e = Extractor(text)
    text = e.remove_stopwords()
    for match in re.finditer(word, text):
        if match.start() == 0:
            index.append(1)
        else:
            subStr = text[0:match.start()-1]
            index.append(len(subStr.split(" "))+1)
    return index  

def writeIndex(inverted_index):
       json.dump(inverted_index, open("C:/Users/sneha/Desktop/python/position.txt", 'w'))

def readIndex():
        index = {}
        index = json.load(open("C:/Users/sneha/Desktop/python/position.txt"))
        return index
 
def getIndex():
    index = {}
    if os.stat("C:/Users/sneha/Desktop/python/position.txt").st_size == 0:
        index = positionalIndex()
        writeIndex(index)
    else:
        index = readIndex()

    return index


def search(query):
    index = getIndex()
    result = set()
    e = Extractor(query)
    query = e.remove_stopwords()
    for count, word in enumerate(query.split()):
        if count == 0:
            firstWord = word
            result = set(index[firstWord][0].keys())
            continue

        dict = {}
        secondWord = word
        dict = index[firstWord][0]
        temp = []
        for key1, value1 in dict.items():
            list = value1[0]
            new_list = [x+1 for x in list]
            secondDict = index[secondWord][0]
            if key1 in secondDict.keys():
                value2 = secondDict[key1]
                if len(set(new_list)&set(value2[0]))!=0:
                    temp.append(key1)

        firstWord = secondWord
        result &= set(temp)            
    return result            
        


if __name__=="__main__":
        query = input("Enter search query: ")
        result = search(query)
        print("\nResults: \n")
        print(result)
        print("\n")
# number one on the billboard 200