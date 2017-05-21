import sys
import string

#CALCULATE PRIOR!!

learnFile = open('nbmodel.txt', 'r')
classifyFile = open('nboutput.txt', 'w')
testDataFile = open(sys.argv[1])

learnFileLines = learnFile.readlines()
testDataFileLines = testDataFile.readlines()

words = []
deceptiveClass = dict()
truthfulClass = dict()
positiveClass = dict()
negativeClass = dict()
wordClasses = [deceptiveClass, truthfulClass, positiveClass, negativeClass]

deceptiveProbability = 0
truthfulProbability = 0
positiveProbability = 0
negativeProbabiity = 0
probabilities = [deceptiveProbability, truthfulProbability, positiveProbability, negativeProbabiity]

deceptivePrior = 0
truthfulPrior = 0
positivePrior = 0
negativePrior = 0



def removeSymbols(strg):
    for char in string.punctuation:
        strg = strg.replace(char, '')
        
    strg = strg.replace('\n', '')
    strg = strg.replace(' ', '') 
    digit_list = ''#"1234567890"
    for char in digit_list:
        strg = strg.replace(char, "")
#     suffixList = ['acy','ance','ence','ism','ist','ity','ty',
#               'ment','ness','ship','sion','tion','ate','ify','fy','ize',
#               'ise','able','ible','esque','ful','ic','ical','ious','ous',
#               'ish','ive','less']
#     for suffix in suffixList:
#         if strg.endswith(suffix):
#             strg = strg[:-len(suffix)]
    
    return strg

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
    
def addWords(word):
    if word not in words:
        words.append(word)

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

def updateProbabilities(word):
    global probabilities 
    for c in wordClasses:
        if word in c:
            index = wordClasses.index(c)            
            probabilities[index] = probabilities[index] + c[word]
            
def getClassification():
    updateProbabilityList()
    firstClass = 'unclassified'
    secondClass = 'unclassified'
    if (deceptiveProbability+deceptivePrior) < (truthfulProbability+truthfulPrior):
        firstClass = 'deceptive'
    else:
        firstClass = 'truthful'
    
    if (positiveProbability+positivePrior) < (negativeProbabiity+negativePrior):
        secondClass = 'positive'
    else:
        secondClass = 'negative'
        
    return (firstClass, secondClass)

def writeToOutputFile(sid, c, fStream):
    fStream.write(sid + ' ' + c[0] + ' ' + c[1] + '\n')
    #fStream.write('deceptive:'+str(deceptiveProbability) + '\n')
    #fStream.write('truthful:'+str(truthfulProbability) + '\n')
    #fStream.write('positive:'+str(positiveProbability) + '\n')
    #fStream.write('negative:'+str(negativeProbabiity) + '\n')


for it in range(0, 4):
    splitLine = learnFileLines[it].split()
    wordClassPrior = splitLine[0]
    priorValue = splitLine[1]
    updatePriors((wordClassPrior,priorValue))


#create internal model
for it in range(4, len(learnFileLines)):
    splitLine = learnFileLines[it].split()
    word = splitLine[0]
    addWords(word)
    classifyWord(splitLine)
    
for it in range(0, len(testDataFileLines)):

    splitLine = testDataFileLines[it].split()

    reviewid = splitLine[0]
    splitLine.pop(0)
    sentence = splitLine
    resetProbabilities()
    for w in sentence:
        processedWord = removeSymbols(w)
        updateProbabilities(processedWord)
    classification = getClassification()
    writeToOutputFile(reviewid, classification, classifyFile)
    

print("size of deceptive class:" + str(len(deceptiveClass)))
print("total words:" + str(len(words)))