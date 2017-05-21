class Word:
    def __init__(self, stringForm, wordCount):
        self.wordCount = wordCount
        self.stringForm = stringForm
        
    def getCount(self):
        return self.wordCount
    
    def incCount(self):
        self.wordCount += 1