import json
import math
import re
from collections import OrderedDict

repoDir = "repoData/"
wordFreqFileName = "/wordFrequencies.pfq"

indexDict = {}

def getFileLines(fileName):
	tempFile = open(fileName, "r")
	tempLines = tempFile.readlines()
	tempFile.close()
	return tempLines

def mergeIndicesToDict(pfqFileName, docId):
	pfqLines = getFileLines(pfqFileName)
	for line in pfqLines:
		lineSplits = line.strip().split("\t")
		if(len(lineSplits) > 0):
			term = lineSplits[0].lower()

			if('a' <= term[0] <= 'z') and re.match("^[A-Za-z0-9_@.-]+$", term):
				termFreq = int(lineSplits[1])
				posting = [docId,termFreq,int(lineSplits[2])] #lineSplits[2] is weightage based on if term is in description
				if(term in indexDict):
					indexDict[term][1].append(posting)
				else:
					indexDict[term] = [0,[posting]]

def updateTfIdf():
	docFreq = 0
	N = len(indexDict)
	for term in indexDict:
		docFreq = len(indexDict[term][1])
		indexDict[term][0] = docFreq
		for i in range(docFreq):
			# modified tfidf score based on text type weightage for that document.
			# indexDict[term][1][i][2] = round((1+math.log(indexDict[term][1][i][1],10)) * math.log(N/docFreq,10) * (1+math.log(indexDict[term][1][i][2]+1,2)),1)
			indexDict[term][1][i][2] = round((1+math.log(indexDict[term][1][i][1],10)) * math.log(N/docFreq,10) * (indexDict[term][1][i][2]+1),1) 

allProjFile = open("projects_meta_data.json")
allProjDict = json.load(allProjFile)
allProjFile.close()

count = 0
for i in range(0,len(allProjDict)):
	folderName = allProjDict[i]["full_name"].replace("/", "-")
	if(os.path.isfile(repoDir+folderName+wordFreqFileName):
		mergeIndicesToDict(repoDir+folderName+wordFreqFileName,folderName)
	else:
		print("No PFQ : "+str(i)+ " : "+folderName)
	if(count%1000 == 0):
		print(count)
	count += 1

updateTfIdf()

charChunkedDict = {}

for term in indexDict:
	if(term[0] in charChunkedDict):
		charChunkedDict[term[0]][term] = indexDict[term]
	else:
		charChunkedDict[term[0]] = {}

def sortByDocFreq(termItem):
	keys = list(termItem.keys())
	return termItem[keys[0]][0]

print(len(charChunkedDict))

for alpha in charChunkedDict:
	charChunkedDict[alpha] = OrderedDict(sorted(charChunkedDict[alpha].items(), key=lambda t: t[1][0], reverse=True))
	if('a' <= alpha <= 'z'):
		indexFileSuffix = alpha	
	else:
		indexFileSuffix = 'special'
	print(alpha)
	json.dump(charChunkedDict[alpha], open(INDEX_FOLDER+'indexDump-'+indexFileSuffix+'.json','w'))


#json.dump(indexDict, open('indexDump.json','w'))

print(len(indexDict))
