from pprint import pprint
import os
from os import listdir
from os.path import isfile, join
import re
import json
import pickle
from extractor import Extractor
import nltk

PATH = "C:/Users/Sneha/Desktop/python/documents"
stopwordsList = ["my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def getFiles():
    onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    return onlyfiles


def extractKeywords():
        keyList = set()
        fileList = getFiles()
        for file in fileList:
                e = Extractor(open(PATH + "/" + file).read())
                keyList |= set(e.rank_words())
                bigram = nltk.bigrams(e.rank_words())
                keyList |= set(map(' '.join, bigram))
        return keyList    

def createIndex():

        inverted = {}
        fileList = getFiles()
        words = extractKeywords()
        for word in words:
                for file in fileList:
                        locations = inverted.setdefault(word, [])
                        if checkWord(word, PATH + "/" + file) == True:
                                locations.append(file)

        return inverted


def checkWord(word, filename):
        if word in (open(filename).read()).lower():
                return True
        else:
                return False


def writeIndex(inverted_index):
       json.dump(inverted_index, open("C:/Users/sneha/Desktop/python/index.txt", 'w'))

def readIndex():
        inverted_index = {}
        inverted_index = json.load(open("C:/Users/sneha/Desktop/python/index.txt"))
        return inverted_index

def writeList(list):
        with open("C:/Users/sneha/Desktop/python/config.txt", 'wb') as f:
                pickle.dump(list, f)

def readList():
        with open("C:/Users/sneha/Desktop/python/config.txt", 'rb') as f:
                list = pickle.load(f)
        return list

def getIndex():
        if os.stat("C:/Users/sneha/Desktop/python/index.txt").st_size == 0:
                inverted_index = createIndex()
                writeIndex(inverted_index)
        else:
                inverted_index = readIndex()

        if os.stat("C:/Users/sneha/Desktop/python/config.txt").st_size == 0:
                writeList(getFiles())
                return inverted_index
        else:
                originalFiles = set(readList())
                updatedFiles = set(getFiles())
                if len(updatedFiles - originalFiles) > 0:
                        newFiles = updatedFiles - originalFiles
                        inverted_index = updateIndex(inverted_index, newFiles)
                        writeIndex(inverted_index)
                        writeList(getFiles())
                        return inverted_index

                else:
                        return inverted_index


def updateIndex(inverted_index, newFiles):
        for word in extractKeywords():
                for file in newFiles:
                        locations = inverted_index.setdefault(word, [])
                        if checkWord(word, PATH + "/" + file) == True:
                                locations.append(file)
        return inverted_index

def search(query):

        inverted_index = getIndex()
        result_set = set()
        operation = None
        for index, word in enumerate(re.split(" +(AND|OR) +",query)):
               
                if index == 0:
                        if word.find('NOT ') == 0:
                                realword = word[4:]
                                current_set = set(inverted_index.get(realword))
                                result_set = set(getFiles())
                                result_set -=current_set
                        else:        
                                if word not in extractKeywords():
                                        print("Invalid Keyword " + word )
                                        break
                                else:
                                        result_set = set(inverted_index.get(word)) 
                        continue
                inverted = False 
                if word in ['AND','OR']:
                        operation = word
                        continue

                if word.find('NOT ') == 0:
                        if operation == 'OR':
                                continue
                        inverted = True
                        realword = word[4:]
                else:
                        realword = word
                        if realword not in extractKeywords():
                                print("Invalid Keyword " + realword )
                                break 

                if operation is not None:
                        current_set = set(inverted_index.get(realword))

                        if operation == "AND":
                                if inverted is True:
                                        result_set -= current_set
                                else:
                                        result_set &= current_set

                        elif operation == "OR":
                                result_set |= current_set

                        operation=None
        return sorted(result_set)


if __name__=="__main__":
        query = "single AND NOT singer"
        query = input("Enter search query: ")
        result = search(query)
        print("\nResults: \n")
        print(result)
        print("\n")