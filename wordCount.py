#! /usr/bin/env python2.7

import sys
import re
import os
import subprocess

inFile = raw_input("Enter source text file\n")
outFile = raw_input("Enter output text file\n")

wordCounter = {}

with open(inFile, 'r') as file:
    for line in file:
        wordList = line.replace('.','').replace(':','').replace(',','').replace('\'','').replace(';','').replace('-',' ').replace('\"','').lower().split()
        for word in wordList:
            if word not in wordCounter:
                wordCounter[word] = 1
            else:
                wordCounter[word] += 1
file.close()

#wordCounter.sort()

with open(outFile, 'w') as oFile:
    for (word, occurance) in sorted(wordCounter.items()):
        oFile.write("%s %.0f\n" % (word, occurance))
oFile.close()
exit()
