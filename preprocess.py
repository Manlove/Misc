from os import listdir
from bs4 import BeautifulSoup
import re
from tkinter.filedialog import askdirectory

##### Opens each reuters file and retrieves the strings, check the number of Topics in each article 
##### and stores unique Topics, their counts and Articles for Articles with a single topic

Topics = {}
Tags = list()
TargetDir = askdirectory()
DirectoryList = listdir(TargetDir)

for files in DirectoryList:
	if (files[-4:] == ".sgm"):
		CompleteString = ""
		with open(TargetDir + files) as InFile:
			for Line in InFile:
				CompleteString += Line

		soup = BeautifulSoup(CompleteString, "html.parser")

		for Item in soup.findAll('reuters'):
			TempTopics = list()
			for ArtTopics in Item.findAll('Topics'):
				if (ArtTopics.get_text() != ''):
					for SingleTopics in ArtTopics.findAll('d'):
						TempTopics.append(SingleTopics)
					if(len(TempTopics) == 1):
						Tags.append(Item)
						if (SingleTopics.get_text() in Topics):
							Topics[SingleTopics.get_text()] = Topics[SingleTopics.get_text()] + 1
						else:
							Topics[SingleTopics.get_text()] = 1

##### finds the 20 most frequent Topics
# TopTopicsCount: stores the count of the top 20 Topics
# TopTopics: stores the string of the top 20 Topics

TopTopicsCount = [0] * 20
TopTopics = [''] * 20
for key in Topics.keys():
	if (Topics[key] > min(TopTopicsCount)):
		TempIndex = TopTopicsCount.index(min(TopTopicsCount))
		TopTopicsCount[TempIndex] = Topics[key]
		TopTopics[TempIndex] = key


##### finds Articles that contain only the top 20 Topics
# ArticleTopics = the Topic of each article
# ArticleBodies = the bodies of each article
# ArticleIDs = the new ID number of each article

ArticleTopics = list()
ArticleBodies = list()
ArticleIDs = list()
NumBodies = 0

for Articles in Tags:
	for Topic in Articles.findAll('Topics'):
		if Topic.get_text() in TopTopics:
			ArticleTopics.append(Topic.get_text())
			for Body in Articles.findAll('body'):
				NumBodies += 1
				Line = re.sub("[^0-9a-zA-Z]+", " ", Body.get_text())
				Line = Line.lower()
				ArticleBodies.append(Line[:-8])
			i = str(Articles)
			TempInd = i.index("newid") + 7
			TempID = ''
			while (i[TempInd] != '"'):
				TempID += i[TempInd]
				TempInd += 1
			ArticleIDs.append(TempID)
			if (len(ArticleTopics) > NumBodies):
				ArticleTopics.pop()
				ArticleIDs.pop()
BagOfWords = list()
BagOfWordsCount = list()

##### splits Articles into words, split by blank space  #####

for i in ArticleBodies:
	for j in i.split():
		j = (j + " ")
		try:
			int(j)
		except:
			if (j not in BagOfWords):
				BagOfWords.append(j)
				BagOfWordsCount.append(1)
			else:
				TempIndex = BagOfWords.index(j)
				BagOfWordsCount[TempIndex] = BagOfWordsCount[TempIndex] + 1
i = 0
while i < len(BagOfWords):
	if BagOfWordsCount[i] < 5:
		BagOfWords.pop(i)
		BagOfWordsCount.pop(i)
	else:
		i += 1
Ind = 0
OutFile = open(TargetDir + "bag.csv", 'w')
for i in ArticleBodies:
        OutFile.write(ArticleIDs[Ind] + "\t" + ArticleTopics[Ind] + "\t")
        TempBag = [0] * len(BagOfWords)
        for j in i.split():
                if (j + " ") in BagOfWords:
                        TempBag[BagOfWords.index(j + " ")] = TempBag[BagOfWords.index(j + " ")] + 1
        for j in range(0, len(TempBag)):
                if TempBag[j] > 0:
                        OutFile.write(str(j) + "," + str(TempBag[j]) + "\t")
        OutFile.write("\n")
        Ind += 1
OutFile.close()
OutFile = open(TargetDir + "bag.clabel", 'w')
for i in BagOfWords:
        OutFile.write(BagOfWords[i] + "\n")
OutFile.close()

##### splits Articles into n-Grams with a sliding window#####

BagOfGrams = list()
NGramBodies = list()
Grams = [3,5,7]
for i in Grams:
        for i in ArticleBodies:
                TempString = ""
                for j in i.split():
                        if (j + " ") in BagOfWords:
                                TempString += j + " "
                NGramBodies.append(TempString)
        for i in NGramBodies:
                for j in range(0, len(i) - NGram + 1):
                        Gram = (i[j:j + NGram] + " ")
                        try:
                                int(Gram)
                        except:
                                if (Gram not in BagOfGrams):
                                        BagOfGrams.append(Gram)

        Ind = 0
        OutFile = open(TargetDir + "char" + str(Grams[i]) + ".csv", 'w')
        for i in NGramBodies:
                OutFile.write(ArticleIDs[Ind] + "\t" + ArticleTopics[Ind] + "\t")
                TempBag = [0] * len(BagOfGrams)
                for j in range(0, len(i) - NGram + 1):
                        Gram = (i[j:j + NGram] + " ")
                        if Gram in BagOfGrams:
                                TempBag[BagOfGrams.index(Gram)] = TempBag[BagOfGrams.index(Gram)] + 1
                for j in range(0, len(TempBag)):
                        if TempBag[j] > 0:
                                OutFile.write(str(j) + "," + str(TempBag[j]) + "\t")
                OutFile.write("\n")
                Ind += 1
        OutFile.close()
        OutFile = open(TargetDir + "char" + str(Grams[i] + ".clabel", 'w')
        for i in BagOfGrams:
                OutFile.write(BagOfGrams[i] + "\n")
        OutFile.close()

