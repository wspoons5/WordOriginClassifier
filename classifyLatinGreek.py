def main():
	latinFile = open("latinProbTable.txt", "r")
	greekFile = open("greekProbTable.txt", "r")
	latinWordFile = open("latinOriginWords.txt", "r", encoding="latin1")
	greekWordFile = open("greekOriginWords.txt", "r", encoding="latin1")

	latinTable, greekTable = loadProbTables(latinFile, greekFile)
	latinWordSet = getWords(latinWordFile)
	greekWordSet = getWords(greekWordFile)

	testClassification(latinWordSet, greekTable, latinTable, "latin")
	testClassification(greekWordSet, greekTable, latinTable, "greek")

	latinFile.close()
	greekFile.close()
	latinWordFile.close()
	greekWordFile.close()

def testClassification(wordSet, greekTable, latinTable, language):
	success = 0
	failure = 0
	for word in wordSet:
		if onlyLetters(word):
			guess = classify(word, greekTable, latinTable)
			if guess == language:
				success += 1
			else:
				failure += 1
	print("{} success rate and {} failure rate out of {} total words.".format(success / (success + failure), failure / (success + failure), success + failure))

def classify(word, greekTable, latinTable):
	greekProb = getProb(word, greekTable)
	latinProb = getProb(word, latinTable)
	if greekProb > latinProb:
		return "greek"
	elif latinProb > greekProb:
		return "latin"
	else:
		return None

def getProb(word, table):
	idx = ord(word[0]) - 97
	prob = table[idx][0]
	for i in range(len(word) - 1):
		priorLetter = word[i] 
		nextLetter = word[i + 1]
		rowIdx = ord(priorLetter) - 97
		colIdx = ord(nextLetter) - 96
		prob *= table[rowIdx][colIdx]
	return prob

def loadProbTables(latinFile, greekFile):
	latinTable = makeEmptyProbTable()
	greekTable = makeEmptyProbTable()

	i = 0
	for line in latinFile:
		lineList = line.split(",")
		for j in range(27):
			latinTable[i][j] = float(lineList[j])
		i += 1

	i = 0
	for line in greekFile:
		lineList = line.split(",")
		for j in range(27):
			greekTable[i][j] = float(lineList[j])
		i += 1

	return latinTable, greekTable

def makeEmptyProbTable():
	table = []
	for i in range(26):
		table.append([0]*27)
	return table

'''
This method takes a file containting a list of newline delimitted words and returns a set containing
all of the words

Args:
infile: The opened file containing the words to be extracted

Returns
wordSet: A set containing strings of all the words in infile
'''
def getWords(infile):
	wordSet = set()
	for line in infile:
		line = line.strip().lower()
		if line != "":
			wordSet.add(line)
	return wordSet

def isLetter(char):
	if 97 <= ord(char) and ord(char) <= 122:
		return True
	else:
		return False

def onlyLetters(word):
	for char in word:
		if not isLetter(char):
			return False
	return True

main()