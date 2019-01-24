def main():
	frenchFile = open("frenchOrigins.txt", "r", encoding = "utf-8")
	frenchSet = getFrenchWords(frenchFile)

def getFrenchWords(infile):
	wordSet = set()
	for line in infile:
		if " " not in line:
			wordSet.add(line.strip().lower()) 
		else:
			wordList = line.split()
			delimitterEncountered = False
			if "," in wordList[0]:
				wordSet.add(wordList[0][:len(wordList[0]) - 1].lower())
			elif wordList[1][0] == "(":
				wordSet.add(wordList[0].lower())

	return wordSet

main()