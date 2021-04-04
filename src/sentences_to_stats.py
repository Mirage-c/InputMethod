'''
预处理：读取res/sentence的txt文件，并且统计其中每一个汉字出现的次数，以及相邻汉字出现的次数。每一个汉字存储一个json字典。
'''
import os
import json

SentenceDir = '..\\preprocessing\\res\\sentence'
outputTarget = '..\\preprocessing\\res\\statics_'
def sToj_2Ele():
    allFiles = []
    dict = {}
    for root, directories, filenames in os.walk(SentenceDir):
        for filename in filenames:
            p = os.path.join(SentenceDir, filename)
            if p.endswith('.txt'):
                allFiles.append(p)

    for f in allFiles:   # 对每一个文件
        print("Processing " + f)
        for line in open(f, 'r+', encoding='utf-8'):  # 对每一个句子
            length = len(line)  # 在预处理中，每个断句必然长度不小于2
            length -= 1
            # 首字符特殊处理
            if u'\u4e00' <= line[0] <= u'\u9fff':
                dict.setdefault(line[0], {})
                dict[line[0]].setdefault('begin', 0)
                dict[line[0]]['begin'] += 1
            for i in range(length-1):  # 对每一个字
                if not u'\u4e00' <= line[i] <= u'\u9fff':  # 非汉字
                    continue
                dict.setdefault(line[i], {})
                dict[line[i]].setdefault('total',0)  # 自身计数
                dict[line[i]]['total'] += 1
                if u'\u4e00' <= line[i+1] <= u'\u9fff':
                    dict[line[i]].setdefault(line[i+1],0)  # 相邻计数
                    dict[line[i]][line[i + 1]] += 1
            # 末尾字符特殊处理
            if u'\u4e00' <= line[length-1] <= u'\u9fff':
                dict.setdefault(line[length-1], {})
                dict[line[length-1]].setdefault('total',0)
                dict[line[length-1]].setdefault('end',0)
                dict[line[length-1]]['end'] += 1
                dict[line[length-1]]['total'] += 1

    # 输出字典
    with open(outputTarget, 'w', encoding='utf-8') as f:
        json.dump(dict,f)
        print("Output json into " + outputTarget)

def sToj_3Ele():
    allFiles = []
    dict = {}
    for root, directories, filenames in os.walk(SentenceDir):
        for filename in filenames:
            p = os.path.join(SentenceDir, filename)
            if p.endswith('.txt'):
                allFiles.append(p)

    for f in allFiles:  # 对每一个文件
        print("Processing " + f)
        for line in open(f, 'r+', encoding='utf-8'):  # 对每一个句子
            length = len(line)  # 在预处理中，每个断句必然长度不小于2
            length -= 1
            # 首字符特殊处理
            if u'\u4e00' <= line[0] <= u'\u9fff':
                dict.setdefault(line[0], {})
                dict[line[0]].setdefault('begin', 0)
                dict[line[0]]['begin'] += 1
            for i in range(length - 1):  # 对每一个字
                if not u'\u4e00' <= line[i] <= u'\u9fff':  # 非汉字
                    continue
                dict.setdefault(line[i], {})
                dict[line[i]].setdefault('total', 0)  # 自身计数
                dict[line[i]]['total'] += 1
                if u'\u4e00' <= line[i + 1] <= u'\u9fff':
                    dict[line[i]].setdefault(line[i + 1], {})  # 相邻计数
                    dict[line[i]][line[i + 1]].setdefault('total',0)
                    dict[line[i]][line[i + 1]]['total'] += 1
                    if i is not length - 2:
                        if u'\u4e00' <= line[i + 2] <= u'\u9fff':
                            dict[line[i]][line[i+1]].setdefault(line[i+2],0)
                            dict[line[i]][line[i+1]][line[i+2]] += 1
            # 末尾字符特殊处理
            if u'\u4e00' <= line[length - 1] <= u'\u9fff':
                dict.setdefault(line[length - 1], {})
                dict[line[length - 1]].setdefault('total', 0)
                dict[line[length - 1]].setdefault('end', 0)
                dict[line[length - 1]]['end'] += 1
                dict[line[length - 1]]['total'] += 1

    # 输出字典
    with open(outputTarget, 'w', encoding='utf-8') as f:
        json.dump(dict, f)
        print("Output json into " + outputTarget)

def sToj_4Ele():
    allFiles = []
    dict = {}
    for root, directories, filenames in os.walk(SentenceDir):
        for filename in filenames:
            p = os.path.join(SentenceDir, filename)
            if p.endswith('.txt'):
                allFiles.append(p)

    for f in allFiles:  # 对每一个文件
        print("Processing " + f)
        for line in open(f, 'r+', encoding='utf-8'):  # 对每一个句子
            length = len(line)  # 在预处理中，每个断句必然长度不小于2
            length -= 1
            # 首字符特殊处理
            if u'\u4e00' <= line[0] <= u'\u9fff':
                dict.setdefault(line[0], {})
                dict[line[0]].setdefault('begin', 0)
                dict[line[0]]['begin'] += 1
            for i in range(length - 1):  # 对每一个字
                if not u'\u4e00' <= line[i] <= u'\u9fff':  # 非汉字
                    continue
                dict.setdefault(line[i], {})
                dict[line[i]].setdefault('total', 0)  # 自身计数
                dict[line[i]]['total'] += 1
                if u'\u4e00' <= line[i + 1] <= u'\u9fff':
                    dict[line[i]].setdefault(line[i + 1], {})  # 相邻计数
                    dict[line[i]][line[i + 1]].setdefault('total',0)
                    dict[line[i]][line[i + 1]]['total'] += 1
                    if i is not length - 2:
                        if u'\u4e00' <= line[i + 2] <= u'\u9fff':
                            dict[line[i]][line[i+1]].setdefault(line[i+2],{})
                            dict[line[i]][line[i + 1]][line[i + 2]].setdefault('total', 0)
                            dict[line[i]][line[i + 1]][line[i + 2]]['total'] += 1
                            if i is not length - 3:
                                if u'\u4e00' <= line[i + 3] <= u'\u9fff':
                                    dict[line[i]][line[i+1]][line[i+2]].setdefault(line[i+3],0)
                                    dict[line[i]][line[i+1]][line[i+2]][line[i+3]] += 1

            # 末尾字符特殊处理
            if u'\u4e00' <= line[length - 1] <= u'\u9fff':
                dict.setdefault(line[length - 1], {})
                dict[line[length - 1]].setdefault('total', 0)
                dict[line[length - 1]].setdefault('end', 0)
                dict[line[length - 1]]['end'] += 1
                dict[line[length - 1]]['total'] += 1

    # 输出字典
    with open(outputTarget, 'w', encoding='utf-8') as f:
        json.dump(dict, f)
        print("Output json into " + outputTarget)

if __name__ == '__main__':
    while True:
        eleNum = input("输入一个数字，代表接下来将要处理数据使其适配于基于字的__元模型：")
        if eleNum == '2':
            outputTarget += eleNum + 'Ele.txt'
            sToj_2Ele()
            break
        elif eleNum == '3':
            outputTarget += eleNum + 'Ele.txt'
            sToj_3Ele()
            break
        elif eleNum == '4':
            outputTarget += eleNum + 'Ele.txt'
            sToj_4Ele()
            break