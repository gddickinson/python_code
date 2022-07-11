# 6.00 Problem Set 3
# 
# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    def testLetter (letter, lettersGuessed):
        i = (len(lettersGuessed))-1           
        while i >= 0:
            if letter == lettersGuessed[i]:
                return True
            i -=1                       
        return False
    
    length = (len(secretWord))
    i = length -1
    correct =0
    while i >= 0:
        #print(secretWord[i])
        if testLetter(secretWord[i], lettersGuessed) == False:
            return False
        else:
            correct +=1
        i -=1
    #print (length)
    #print (correct)    
    #print (i)
    if correct == length:
        return True   
        
    else:
        return False



def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    def testLetter (letter, lettersGuessed):
        i = (len(lettersGuessed))-1           
        while i >= 0:
            if letter == lettersGuessed[i]:
                return letter
            i -=1                       
        return ' _'
    
    length = (len(secretWord))
    i = length -1
    ans =""
    while i >= 0:
        ans = ans + testLetter(secretWord[i], lettersGuessed)
        i -=1
    return ans[::-1]



def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    import string
    alpha = string.ascii_lowercase
    def testLetter (letter, lettersGuessed):
        i = (len(lettersGuessed))-1           
        while i >= 0:
            if letter == lettersGuessed[i]:
                return True
            i -=1                       
        return False
    
    ans = ''    
    i = 25
    while i >=0:
        if testLetter(alpha[i], lettersGuessed) == True:
            addLetter = ''
        else:
            addLetter = alpha[i]
        ans = ans + addLetter
        i-=1
        
    return ans[::-1]
    

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    
    # FILL IN YOUR CODE HERE...
    def getGuess(lettersGuessed):
        print('You have %d guesses left.') % guessesLeft
        print('Available letters:' +str(getAvailableLetters(lettersGuessed)))
        guess = raw_input ('Please guess a letter: ')
        guess = guess.lower()
        return guess

    def rightGuess(secretWord, lettersGuessed):
        print ('Good guess: ' +str((getGuessedWord(secretWord, lettersGuessed))))
        print("--------")
        return
        
    def wrongGuess(secretWord, lettersGuessed):
        print ('Oops! That letter is not in my word: ' +str(getGuessedWord(secretWord, lettersGuessed)))
        print("--------")
        return 1
        
    def allreadyGuessed(secretWord, lettersGuessed):
        print ('Oops! You\'ve already guessed that letter: '+str(getGuessedWord(secretWord, lettersGuessed)))
        print("--------")        
        return
    
    def compareGuess(guess, secretWord):
        i = (len(secretWord)) -1         
        while i >= 0:
    
            if guess == secretWord[i]:
                #print (guess)
                return True
            i -= 1    
        return False
        
        
    print ('Welcome to the game, Hangman!')
    wordLength = len(secretWord)
    guessesLeft = 8
    lettersGuessed = []
    print ('I am thinking of a word that is %d letters long.') % wordLength
    print ('----------')
    
    
    #main loop
    while isWordGuessed(secretWord,lettersGuessed) == False:
        guess = getGuess(lettersGuessed)
        oldAvailableLetters = (getAvailableLetters(lettersGuessed))        
        lettersGuessed.append(guess)
        availableLetters = (getAvailableLetters(lettersGuessed))
        #print (len(oldAvailableLetters), len(availableLetters))
        
        ##for same guess
        if len(oldAvailableLetters) == len(availableLetters):
            allreadyGuessed(secretWord, lettersGuessed)
        
        ##for new guesses    
        else:
            if compareGuess(guess, secretWord) == True:
                rightGuess(secretWord, lettersGuessed)
            else:
                wrongGuess(secretWord, lettersGuessed)
                guessesLeft -=1
                if guessesLeft == 0:
                    print ('Sorry, you ran out of guesses. The word was ' +str(secretWord))
                    break
    if guessesLeft >0:
        print ('Congratulations you won!')

# When you've completed your hangman function, uncomment these two lines
# and run this file to test! (hint: you might want to pick your own
# secretWord while you're testing)


secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
