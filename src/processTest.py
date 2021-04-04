'''
将输入法测试集.txt分为两个文件，一个是input.txt，一个是standardOutput.txt
'''

import os
FileToOpen = '..\\data\\输入法测试集.txt'
InputRoot = '..\\data\\input.txt'
OutputRoot = '..\\data\\standardOutput.txt'
lineNum = 0

tmpInput = ''
tmpOutput = ''

for line in open(FileToOpen,'r+',encoding='utf-8'):
    if lineNum % 2 == 0:
        tmpInput += line
    else:
        tmpOutput += line
    lineNum += 1

input = open(InputRoot, 'w', encoding='utf-8')
input.write(tmpInput)
input.close()
output = open(OutputRoot, 'w', encoding='utf-8')
output.write(tmpOutput)
output.close()