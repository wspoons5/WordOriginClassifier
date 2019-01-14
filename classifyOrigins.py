import math

def main():
	infile = open("greekLatinOrigins.txt", "r", encoding = "utf-8")
	greekSet = set()
	latinSet = set()
	n = 2
	for line in infile:
		try:
			lineList = line.strip().lower().split("\t")
			wordList = lineList[4].split(",")
			origin = lineList[2]
			if origin == "greek":
				for word in wordList:
					greekSet.add(word.strip())
			if origin == "latin":
				for word in wordList:
					latinSet.add(word.strip())

		except IndexError:
			dumb = True
	latinLetterMap = getLanguageGramFrequency(n, latinSet)
	greekLetterMap = getLanguageGramFrequency(n, greekSet)
	
	noneCount = 0
	count = len(greekSet)
	success = 0
	failure = 0

	for word in greekSet:
		origin = getOrigin(n, word, greekLetterMap, latinLetterMap)
		if origin == "Greek":
			success += 1
		elif origin == "Latin":
			failure += 1

		if origin == "None":
			noneCount += 1

	print("GREEK\n{} ({:f}) Classified correctly\n{} ({:f}) Classified incorrectly\n{} ({:f}) Could not be classified".format(success, success/count,
		          	                       																				      failure, failure/count,
		                            																				          noneCount, noneCount/count))

	noneCount = 0
	count = len(latinSet)
	success = 0
	failure = 0
	for word in latinSet:
		origin = getOrigin(n, word, greekLetterMap, latinLetterMap)
		if origin == "Latin":
			success += 1
		elif origin == "Greek":
			failure += 1

		if origin == "None":
			noneCount += 1

	print("LATIN\n{} ({:f}) Classified correctly\n{} ({:f}) Classified incorrectly\n{} ({:f}) Could not be classified".format(success, success/count,
		          	                       																				      failure, failure/count,
		                            																				          noneCount, noneCount/count))

def getOrigin(n, word, greekLetterMap, latinLetterMap):
		observed, greekExpected, latinExpected = getExpectedAndTheoreticalDists(n, word, greekLetterMap, latinLetterMap)
		latinGstat = computeGStatistic(observed, latinExpected)
		greekGstat = computeGStatistic(observed, greekExpected)

		if latinGstat > greekGstat:
			return "Greek"
		elif greekGstat > latinGstat:
			return "Latin"
		else:
			return "None"

def computeGStatistic(observed, expected):
	## Check observed and expected have the same number of 
	n = len(observed)
	stat = 0
	for i in range(n):
		stat += expected[i] * math.log(observed[i] / expected[i])
	return 2*stat

def getExpectedAndTheoreticalDists(n, word, greekMap, latinMap):
	expected = {}	
	for i in range((len(word) - n) + 1):
		seq = ""
		for j in range(n):
			seq += word[i + j]
		allLettersAlpha = True
		for k in range(n):
			if 97 <= ord(seq[k]) and ord(seq[k]) <= 122:
				pass
			else:
				allLettersAlpha = False
		if allLettersAlpha:
			if seq in expected.keys():
				expected[seq] += 1
			else:
				expected.update({seq:1})
		seq = ""

	observed = list(expected.values())
	categoryCount = len(expected.keys())
	latinExpected = [categoryCount]*categoryCount
	greekExpected = [categoryCount]*categoryCount


	i = 0
	for key in expected.keys():
		latinExpected[i] *= latinMap[key]
		greekExpected[i] *= greekMap[key]
		i += 1

	return observed, latinExpected, greekExpected

def getLanguageGramFrequency(n, wordSet):
	gramMap = nGramMap(n)
	for word in wordSet:
		charSeq = ""
		for i in range((len(word) - n) + 1):
			for j in range(n):
				charSeq += word[i + j]
			if charSeq in gramMap.keys():
				gramMap[charSeq] += 1
			charSeq = ""

	totalCount = sum(gramMap.values())
	for key in gramMap.keys():
		if gramMap[key] == 0:
			gramMap[key] = 0.0000000000000000000000000000000001 ## Handles divide by zero errors for stat computation
		else:
			gramMap[key] /= totalCount

	return gramMap

def nGramMap(n):

	gramMap = {}
	if n == 1:
		for i in range(26):
			string = "{}".format(chr(i + 97))
			gramMap.update({string: 0})
	elif n == 2:
		for i in range(26):
			for j in range(26):
				string = "{}{}".format(chr(i + 97), chr(j + 97))
				if string not in gramMap.keys():
					gramMap.update({string: 0})

	return gramMap
  
main()