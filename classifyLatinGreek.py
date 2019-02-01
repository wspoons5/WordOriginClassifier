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

'''
This method tests the classification system on a word set of latin or greek words and prints the
test output to the screen.

Input:
wordSet: A set of unique words all of either Latin or Greek origin
greekTable: A 26x27 matrix containing the conditional letter counts for English words of Greek origin. 
latinTable: A 26x27 matrix containing the conditional letter counts for English words of Latin origin.
language: A string that is either "greek" or "latin" which represents the language origin of the words
          in wordSet
'''
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
	print("{:f} success rate and {:f} failure rate out of {} total words.".format(success / (success + failure), failure / (success + failure), success + failure))

'''
This method takes an input word and classifies it as either of Greek or Latin origin. It classifies
a word as a certain origin by taking conditional letter frequencies for words of that origin then 
calculates the probability of observing the assortment of letters in the input for both the Greek and
Latin conditional frequencies. It then classifies the word based on whichever language has the highest
probability. If the probabilities are identical, then it classifies it as None.

Input:
word: A string containing an English word.
greekTable: A 26x27 matrix containing the conditional letter counts for English words of Greek origin. 
latinTable: A 26x27 matrix containing the conditional letter counts for English words of Latin origin.

Return:
returns the string "greek" if the origin is determined to be Greek. Returns the string "latin" if the 
origin is determined to be "latin". Returns None if the origin could not be determined.  
'''
def classify(word, greekTable, latinTable):
	greekProb = getProb(word, greekTable)
	latinProb = getProb(word, latinTable)
	if greekProb > latinProb:
		return "greek"
	elif latinProb > greekProb:
		return "latin"
	else:
		return None
'''
This method takes an input word and a table of conditional letter frequencies and calculates the probability
of observing the input word given the conditional letter frequencies.

Input:
word: A string containing a word
table: A 26x27 matrix containing the conditional letter frequencies as probabilities. Each row represents a 
       letter as an element of ascii[a-z] with row 0 corresponding to "a" and row 25 corresponding to "z".
       the first column represents the unconditional letter frequencies of that letter. Then each row after 
       the first represents the conditional probability of observing the column letter given the row letter.
       For example, the probability contained in the cell table[0][2] represents the probability of the letter
       "b" following the letter "a" and the cell table[1][3] represents the probability of the letter "c"
       following "b".

Return. A float representing the conditional probability of observing the input word given the input probability
        table.  
'''
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

'''
This method takes the input text files containing the probability tables for Greek and Latin and
processes them into two 26x27 matrices.

Input:
latinFile: An opened file for reading containing the conditional probability table for latin
greekFile: An opened file for reading containing the conditional probability table for Greek

Return: Returns two 26x27 matrices containing the Latin and Greek probability tables
'''
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

'''
This method returns a 26x27 matrix initialized with zeroes
'''
def makeEmptyProbTable():
	table = []
	for i in range(26):
		table.append([0]*27)
	return table

'''
This method takes a file containting a list of newline delimitted words and returns a set containing
all of the words

Input
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

'''
This method takes a char and returns True if the char is an element of ascii[a-z] and returns False otherwise
'''
def isLetter(char):
	if 97 <= ord(char) and ord(char) <= 122:
		return True
	return False

'''
This method takes a string and returns True if every char in the string is an element of ascii[a-z] 
and returns False otherwise
'''
def onlyLetters(word):
	for char in word:
		if not isLetter(char):
			return False
	return True

main()