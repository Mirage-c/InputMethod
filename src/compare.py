'''
将output与standardOutput作比较，输出句正确率以及字正确率
'''

import os

def compare():
    OutputFile = '..\\data\\output.txt'
    StandardOutput = '..\\data\\standardOutput.txt'
    OutputTarget = '..\\data\\res.txt'

    outputString = ''
    output = []
    grandTruth = []
    correctSentence = 0
    correctWord = 0
    totalWord = 0
    totalSentence = 0
    for line in open(OutputFile,'r+',encoding='utf-8'):
        output.append(line)
    for line in open(StandardOutput,'r+',encoding='utf-8'):
        grandTruth.append(line)
    totalSentence = len(output)
    for i in range(totalSentence):
        if(output[i] == grandTruth[i]):
            correctSentence += 1
        sentenceLength = len(output[i])
        totalWord += sentenceLength
        for j in range(sentenceLength):
            if output[i][j] == grandTruth[i][j]:
                correctWord += 1
    outputString += 'Word correct rate: ' + str(correctWord/totalWord) + '\n'
    outputString += 'Sentence correct rate: ' + str(correctSentence/totalSentence) + '\n'
    #with open(OutputTarget, 'a', encoding='utf-8') as f:
    #    f.write(outputString)
    print(outputString)

compare()