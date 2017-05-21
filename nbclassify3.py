import sys
import string


#set up files to open and write to
learnFile = open('nbmodel.txt', 'r') # model file containing prior and word probabilities
classifyFile = open('nboutput.txt', 'w') # file to write sentence classification info to
testDataFile = open(sys.argv[1]) # file containing sentences to classify

# Read lines from files
learnFileLines = learnFile.readlines()
testDataFileLines = testDataFile.readlines()

# Variables to hold word and probability info
words = []
deceptiveClass = dict()
truthfulClass = dict()
positiveClass = dict()
negativeClass = dict()

# Array of dictionaries, used to iterate through dictionaries
wordClasses = [deceptiveClass, truthfulClass, positiveClass, negativeClass]

# Probabilities (for each sentence) (updated every new sentence)
deceptiveProbability = 0
truthfulProbability = 0
positiveProbability = 0
negativeProbabiity = 0
probabilities = [deceptiveProbability, truthfulProbability, positiveProbability, negativeProbabiity]

# Prior values for each class
deceptivePrior = 0
truthfulPrior = 0
positivePrior = 0
negativePrior = 0

# Remove symbols, numbers, and spaces from string
def removeSymbols(strg):
    for char in string.punctuation:
        strg = strg.replace(char, '')
        
    strg = strg.replace('\n', '')
    strg = strg.replace(' ', '') 
    digit_list = "1234567890"
    for char in digit_list:
        strg = strg.replace(char, "")    
    return strg

# extract Prior value info from prior tuple
def updatePriors(priorTuple):
    global deceptivePrior
    global truthfulPrior
    global positivePrior
    global negativePrior
    class_name = priorTuple[0]
    class_prior = priorTuple[1]    
    if class_name == 'deceptivePrior':
        deceptivePrior = float(class_prior)
    if class_name == 'truthfulPrior ':
        truthfulPrior  = float(class_prior)
    if class_name == 'positivePrior':
        positivePrior = float(class_prior)
    if class_name == 'negativePrior':
        negativePrior = float(class_prior)

# Put words and probabilities into respective dictionaries
def classifyWord(wordInfo):
    word = wordInfo[0]
    wordClass = wordInfo[1]
    wordProbability = wordInfo[2]
    
    if wordClass == 'deceptive':
        deceptiveClass[word] = float(wordProbability)
    elif wordClass == 'truthful':
        truthfulClass[word] = float(wordProbability)
    elif wordClass == 'positive':
        positiveClass[word] = float(wordProbability)
    elif wordClass == 'negative':
        negativeClass[word] = float(wordProbability)
    else:
        print("Critical Classification Error!")
    
# Add given word to list of unique words
def addWords(word):
    if word not in words:
        words.append(word)

# Reset all probabilites (call when evaluating new sentence)
def resetProbabilities():    
    global deceptiveProbability    
    global truthfulProbability
    global positiveProbability
    global negativeProbabiity
    global probabilities 
    deceptiveProbability = 0
    truthfulProbability = 0
    positiveProbability = 0
    negativeProbabiity = 0
    probabilities = [deceptiveProbability, truthfulProbability, positiveProbability, negativeProbabiity]

# Update probability values from 'probabilities' array
def updateProbabilityList():
    global probabilities
    global deceptiveProbability    
    global truthfulProbability
    global positiveProbability
    global negativeProbabiity
    deceptiveProbability = probabilities[0]
    truthfulProbability = probabilities[1]
    positiveProbability = probabilities[2]
    negativeProbabiity = probabilities[3]

# update respective probabilities with given word probability
def updateProbabilities(word):
    global probabilities 
    for c in wordClasses:
        if word in c:
            index = wordClasses.index(c)
            probabilities[index] = probabilities[index] + c[word]
            
# Check probabilities and determine the class
def getClassification():
    updateProbabilityList()
    firstClass = 'unclassified'
    secondClass = 'unclassified'
    if (deceptiveProbability+deceptivePrior) > (truthfulProbability+truthfulPrior):
        firstClass = 'deceptive'
    else:
        firstClass = 'truthful'
    
    if (positiveProbability+positivePrior) > (negativeProbabiity+negativePrior):
        secondClass = 'positive'
    else:
        secondClass = 'negative'
        
    return (firstClass, secondClass)

# Write results to output file
def writeToOutputFile(sid, c, fStream):
    fStream.write(sid + ' ' + c[0] + ' ' + c[1] + '\n')
#     fStream.write('deceptive:'+str(deceptiveProbability) + '\n')
#     fStream.write('truthful:'+str(truthfulProbability) + '\n')
#     fStream.write('positive:'+str(positiveProbability) + '\n')
#     fStream.write('negative:'+str(negativeProbabiity) + '\n')

# Read in prior values
for it in range(0, 4):
    splitLine = learnFileLines[it].split()
    wordClassPrior = splitLine[0]
    priorValue = splitLine[1]
    updatePriors((wordClassPrior,priorValue))


#create internal model of words + probabilities
for it in range(4, len(learnFileLines)):
    splitLine = learnFileLines[it].split()
    word = splitLine[0]
    addWords(word)
    classifyWord(splitLine)
    
# Iterate through sentences of test file and determine class using the internal model
for it in range(0, len(testDataFileLines)):
    splitLine = testDataFileLines[it].split()
    reviewid = splitLine[0]
    splitLine.pop(0)
    sentence = splitLine
    resetProbabilities()
    for w in sentence:
        processedWord = removeSymbols(w.lower())
        updateProbabilities(processedWord)
    classification = getClassification()
    writeToOutputFile(reviewid, classification, classifyFile)    

# print("size of deceptive class:" + str(len(deceptiveClass)))
# print("total words:" + str(len(words)))