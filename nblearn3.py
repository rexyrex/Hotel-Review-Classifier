import sys
import string
import math


#add word to class        
def updateClasses(word, classification):
    if classification[0] == 'deceptive':
        if word in deceptiveClass:
            deceptiveClass[word] += 1
        else:
            deceptiveClass[word] = 1
    else:
        if word in truthfulClass:
            truthfulClass[word] += 1
        else:
            truthfulClass[word] = 1
        
    if classification[1] == 'positive':
        if word in positiveClass:
            positiveClass[word] += 1
        else:
            positiveClass[word] = 1
    else:
        if word in negativeClass:
            negativeClass[word] += 1
        else:
            negativeClass[word] = 1

# Remove words that have low or high frequency in given class
def cleanClass(wordClass):
    d = dict(wordClass)
    for k,v in d.items():
        if v <10 or v>1000:
            del wordClass[k]
    
# Remove low/high freq words and delete words that exist in all 4 classes
def cleanClasses():
    cleanClass(deceptiveClass)
    cleanClass(truthfulClass)
    cleanClass(positiveClass)
    cleanClass(negativeClass)
    maxWords = max([len(deceptiveClass), len(truthfulClass), len(positiveClass), len(negativeClass)])
    theClass = {}
    for maxClass in classTypes:
        if len(maxClass) == maxWords:
            theClass= dict(maxClass)
    for k in theClass.keys():
        keyInClassCount = 0
        for iterClass in classTypes:
            if k in iterClass:
                keyInClassCount+=1
        if keyInClassCount ==4:
            print('deleting:' + k)
            for iterClass in classTypes:
                del iterClass[k]

# return total number of word instances in given class
def getClassWordCount(wordClass):
    count = 0
    for value in wordClass.values():
        count += value
    return count

# Get the log probability of a word in given class
def getWordProbability(word, wordClass):
    if word in wordClass:
        c = wordClass[word]
    else:
        c = 0
    return math.log(float((c+1)) / (len(words) + getClassWordCount(wordClass)))

# Export Model : First 4 lines are prior values, rest are word + class + probabilities
def exportModel():
    exportFile = open("nbmodel.txt", 'w')
    updatePriors()
    for classType in classTypes:
        exportFile.write(getClassName(classType) + 'Prior ' + str(priorsDicitonary[getClassName(classType)]) + '\n')
    
    
    for classType in classTypes:
        for word in words: #classType.keys():
            exportFile.write(word + ' ' + getClassName(classType) + ' '+ str(getWordProbability(word, classType)) + '\n')            
    exportFile.close()
    
# Update prior for each class
def updatePriors():
    for classType in classTypes:
        if getClassName(classType) == 'deceptive':
            priorsDicitonary[getClassName(classType)] = math.log(float(deceptiveCount) / totalReviewsCount)
#             print("deceptiveCount = " + str(float(deceptiveCount)) )
#             print("total = " + str(totalReviewsCount) )
#             print("calculated:" + str(math.log(float(deceptiveCount) / totalReviewsCount)))
        if getClassName(classType) == 'truthful':
            priorsDicitonary[getClassName(classType)] = math.log(float(truthfulCount) / totalReviewsCount)
        if getClassName(classType) == 'positive':
            priorsDicitonary[getClassName(classType)] = math.log(float(positiveCount) / totalReviewsCount)
        if getClassName(classType) == 'negative':
            priorsDicitonary[getClassName(classType)] = math.log(float(negativeCount) / totalReviewsCount)

# return string form of class
def getClassName(wordClass):
    if wordClass == deceptiveClass:
        return 'deceptive'
    elif wordClass == truthfulClass:
        return 'truthful'
    elif wordClass == positiveClass:
        return 'positive'
    elif wordClass == negativeClass:
        return 'negative'
    else:
        return 'UNKNOWN CLASS'

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

#list of stop words
unwantedWordsList = ['', ' ', 'a', 'the', 'from', '\n', 'and', 'to','i','we','of','hotel','all','when','where','they',
                     'with','at','not','what','my','you','very','this','as','be','room','stay','our','had','were','on','would',
                     'was','service','is','if','them','their','themselves']    

# Check if word is in stop word list
def isUnwantedWord(strg):
    for w in unwantedWordsList:
        if strg == w:
            return True        
    return False

# Count instances of each class
def countLabels(lb):
    global totalReviewsCount
    global deceptiveCount
    global truthfulCount
    global positiveCount
    global negativeCount
    
    totalReviewsCount += 1
    
    if lb[0] == 'deceptive':
        deceptiveCount += 1
    if lb[0] == 'truthful':
        truthfulCount += 1
    if lb[1] == 'positive':
        positiveCount += 1
    if lb[1] == 'negative':
        negativeCount += 1    
    
totalReviewsCount =0
deceptiveCount =0
truthfulCount=0
positiveCount=0
negativeCount=0

deceptiveClass = dict()
truthfulClass = dict()
positiveClass = dict()
negativeClass = dict()
classTypes = [deceptiveClass, truthfulClass, positiveClass, negativeClass]

priorsDicitonary = {}

# Read in text file (sentences) and label file (classification for each sentence)
trainTextFile = open(sys.argv[1])
trainLabelFile = open(sys.argv[2])

trainTextLines = trainTextFile.readlines()
trainLabelLines = trainLabelFile.readlines()

words = []
ids = []
sentenceDict = {}
labelDict = {}

#print("Learning... Please wait!")

for it in range(0, len(trainTextLines)):    
    sentence = trainTextLines[it].split()
    ids.append(sentence[0])
    sentence.pop(0)
    sentenceDict[ids[it]] = sentence
    tmp = trainLabelLines[it].split()
    tmp.pop(0)
    labelDict[ids[it]] = tmp
    countLabels(labelDict[ids[it]])
    for it2 in range(0, len(sentence)):
        foundWord = sentence[it2].lower()
        foundWord = removeSymbols(foundWord)
        if (foundWord not in words) and (not isUnwantedWord(foundWord)):
            words.append(foundWord)
        if not isUnwantedWord(foundWord):
            updateClasses(foundWord, labelDict[ids[it]])

# disabled cleanClasses() as F1 score is higher without
#cleanClasses()
trainTextFile.close()
trainLabelFile.close()

# print('n. of unique words: ' + str(len(words)))
# print('n. of truthfulClass: ' + str(len(truthfulClass)))
# print('n. of deceptiveClass: ' + str(len(deceptiveClass)))
# print('n. of positiveClass: ' + str(len(positiveClass)))
# print('n. of negativeClass: ' + str(len(negativeClass)))
# 
# print (' total for truthful : ' + str(getClassWordCount(truthfulClass)))
# print('probability that zzeess is truthful:' + str(getWordProbability('good', truthfulClass)))
# print('N. of deceptive sentences:' + str(deceptiveCount) + '/' + str(totalReviewsCount))
# print('N. of truthful sentences:' + str(truthfulCount) + '/' + str(totalReviewsCount))
# print('N. of positive sentences:' + str(positiveCount) + '/' + str(totalReviewsCount))
# print('N. of negative sentences:' + str(negativeCount) + '/' + str(totalReviewsCount))

exportModel()