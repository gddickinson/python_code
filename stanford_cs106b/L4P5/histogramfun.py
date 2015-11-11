import pylab

# You may have to change this path
WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """

    vowelPropList = []
    
    def vowelProp(word):
        numVowels = 0.0          
        vowelList = ['a','e','i','o','u']
        wordLength = len(word)
        for i in range(wordLength):
            for vowel in vowelList:
                if vowel == word[i]:
                    numVowels += 1

        return float(numVowels/wordLength)


    for word in wordList:
        vowelPropList.append(vowelProp(word))
      
    
    pylab.hist(vowelPropList,numBins)
    print(sum(vowelPropList)/len(vowelPropList))
            
            

if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
