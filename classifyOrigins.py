from scipy import stats
import itertools

def main():
	infile = open("greekLatinOrigins.txt", "r", encoding = "utf-8")
	greekSet = set()
	latinSet = set()
	unclassifiedSet = set()
	gramStringMap = nGramMap(2)

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
	latinLetterMap = getLanguageGramFrequency(2, latinSet)
	greekLetterMap = getLanguageGramFrequency(2, greekSet)
	
	noneCount = 0
	count = len(greekSet)
	success = 0
	failure = 0
	for word in greekSet:
		origin = getOrigin(2, word, latinLetterMap, greekLetterMap)
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
		origin = getOrigin(2, word, latinLetterMap, greekLetterMap)
		if origin == "Latin":
			success += 1
		elif origin == "Greek":
			failure += 1

		if origin == "None":
			noneCount += 1

	print("LATIN\n{} ({:f}) Classified correctly\n{} ({:f}) Classified incorrectly\n{} ({:f}) Could not be classified".format(success, success/count,
		          	                       																				      failure, failure/count,
		                            																				          noneCount, noneCount/count))
	
def getOrigin(n, word, latinLetterMap, greekLetterMap):
	greekStat, greekPval = getChiSquare(n, word, greekLetterMap)
	latinStat, latinPval = getChiSquare(n, word, latinLetterMap)
	
	if greekPval > latinPval:
		return "Greek"
	elif latinPval > greekPval:
		return "Latin"
	else:
		return "None"

def getChiSquare(n, word, expectedMap):
	wordSeqMap = {}
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
			if seq in wordSeqMap.keys():
				wordSeqMap[seq] += 1
			else:
				wordSeqMap.update({seq:1})
		seq = ""

	observed = list(wordSeqMap.values())
	expected = [None]*len(wordSeqMap.keys())
	i = 0
	for key in wordSeqMap:
		expected[i] = int(expectedMap[key] * 1000)
		i += 1

	return stats.chisquare(observed, expected)


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
		gramMap[key] /= totalCount

	return gramMap


	# for line in infile:
	# 	try:
	# 		lineList = line.strip().lower().split("\t")
	# 		wordList = lineList[4].split(",")
	# 		origin = lineList[2]
	# 		if origin == "greek":
	# 			for word in wordList:
	# 				greekSet.add(word.strip())
	# 		if origin == "latin":
	# 			for word in wordList:
	# 				latinSet.add(word.strip())

	# 	except IndexError:
	# 		dumb = True
	# latinLetterMap = getWordCount(latinSet)
	# greekLetterMap = getWordCount(greekSet)

	# # for key in latinLetterMap.keys():
	# # 	print("{}: {:f} (Latin) {:f} (Greek)".format(key, latinLetterMap[key], greekLetterMap[key])) 
	# correctCount = 0
	# incorrectCount = 0
	# for word in greekSet:
	# 	wordClass = classifyWordByLetter(word)
	# 	if wordClass == "cnbd":
	# 		unclassifiedSet.add(word)
	# 	if wordClass == "Greek":
	# 		correctCount += 1
	# 	else:
	# 		incorrectCount += 1
	# # print("Greek: {:f} Correct {:f}: Incorrect".format(correctCount / (correctCount + incorrectCount), incorrectCount / (correctCount + incorrectCount)))

	# correctCount = 0
	# incorrectCount = 0
	# for word in latinSet:
	# 	wordClass = classifyWordByLetter(word)
	# 	if wordClass == "cnbd":
	# 		unclassifiedSet.add(word)
	# 	if wordClass == "Latin":
	# 		correctCount += 1
	# 	else:
	# 		incorrectCount += 1
	# # print("Latin: {} Correct {}: Incorrect".format(correctCount / (correctCount + incorrectCount), incorrectCount / (correctCount + incorrectCount)))
	# print(unclassifiedSet)

def nGramMap(n):
	gramMap = {}
	letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
	           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	combinations = itertools.permutations(letters, n)
	for i in range(26):
		for j in range(26):
			string = "{}{}".format(letters[i], letters[j])
			if string not in gramMap.keys():
				gramMap.update({string: 0})
			else:
				dumb = True

	return gramMap
  

def classifyWordByLetter(word):
	latinFrequency = {"a": 0.089015, "b": 0.014957, "c": 0.051667, "d": 0.028309, "e": 0.112730, "f": 0.011106,
	                  "g": 0.014110, "h": 0.004951, "i": 0.101326, "j": 0.002795, "k": 0.000297, "l": 0.050834,
	                  "m": 0.033230, "n": 0.084956, "o": 0.071397, "p": 0.028249, "q": 0.004252, "r": 0.075813,
	                  "s": 0.062708, "t": 0.084273, "u": 0.049347, "v": 0.017321, "w": 0.000431, "x": 0.004237,
	                  "y": 0.012192, "z": 0.000387}

	greekFrequency = {"a": 0.084660, "b": 0.010549, "c": 0.055573, "d": 0.022768, "e": 0.089005, "f": 0.000209, 
	                  "g": 0.024400, "h": 0.054283, "i": 0.082838, "j": 0.000000, "k": 0.001935, "l": 0.038611,
	                  "m": 0.047491, "n": 0.048914, "o": 0.117750, "p": 0.057869, "q": 0.000095, "r": 0.061816,
	                  "s": 0.051815, "t": 0.070468, "u": 0.016052, "v": 0.000228, "w": 0.000019, "x": 0.005445,
	                  "y": 0.042690, "z": 0.003624}

	wordList = [1]*26
	for letter in word:
		if 97 <= ord(letter) and ord(letter) <= 122:
			wordList[ord(letter) - 97] += 1
	
	expectedLatin = list(latinFrequency.values())
	expectedGreek = list(greekFrequency.values())

	for i in range(26):
		expectedGreek[i] = int(round(expectedGreek[i] * len(word))) + 1
		expectedLatin[i] = int(round(expectedLatin[i] * len(word))) + 1

	greekStat, greekPval = stats.chisquare(wordList, expectedGreek)
	latinStat, latinPval = stats.chisquare(wordList, expectedLatin)

	if latinPval > greekPval:
		return "Latin"
	elif greekPval > latinPval:
		return "Greek"
	else:
		return "cnbd"
def getWordCount(wordList):
	wordMap = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0,
	           "i": 0, "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0,
	           "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0,
	           "y": 0, "z": 0}

	for word in wordList:
		for char in word:
			if 97 <= ord(char) and ord(char) <= 122:
				wordMap[char] += 1
	totalChars = sum(wordMap.values())
	for key in wordMap.keys():
		wordMap[key] = wordMap[key] / totalChars

	return wordMap

main()