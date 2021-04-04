'''
运行方式示例：python pinyin.py ./input.txt ./output.txt
'''
import sys, re, os, json, math, time
from openpyxl import Workbook

class node():
    def __init__(self, hanzi, parent, minDistance):
        self.hanzi = hanzi
        self.parent = parent
        self.minDistance = minDistance

    def __str__(self):
        return '(' + self.parent + ')' + self.hanzi + ' : ' + self.minDistance

    def __repr__(self):
        return self.hanzi


root = node(None, None, 0)
InputFile = sys.argv[1]
OutputFile = sys.argv[2]
StaticsFile =   '..\\preprocessing\\res\\statics_'
Pinyin2HanziFile =  '..\\preprocessing\\res\\pinyin_hanzi.txt'
Pinyin2Hanzi = {}
Statics = {}
possibilityOfHanzi = {}
eleNum = 0
totalNum = 0
totalNum_begin = 0
totalNum_end = 0
_lambda = 0.0
_miu = 0.0
_phi = 0.0
lambdaTable = [0.91]
miuTable = [6.1]
phiTable = [5]
wb = Workbook()
workSheet = wb.active

def getPossibility_2Ele(hanzi1,hanzi2):
    try:
        possibility_2Ele = Statics[hanzi1][hanzi2] / Statics[hanzi1]['total']
    except KeyError:
        possibility_2Ele = 0
    except TypeError:
        possibility_2Ele = Statics[hanzi1][hanzi2]['total'] / Statics[hanzi1]['total']
    return possibility_2Ele

def getPossibility_3Ele(hanzi1,hanzi2,hanzi3):
    try:
        possibility_3Ele = Statics[hanzi1][hanzi2][hanzi3] / Statics[hanzi1][hanzi2]['total']
    except KeyError:
        possibility_3Ele = 0
    except TypeError:
        possibility_3Ele = Statics[hanzi1][hanzi2][hanzi3]['total'] / Statics[hanzi1][hanzi2]['total']
    return possibility_3Ele

def getPossibility_4Ele(hanzi1,hanzi2,hanzi3,hanzi4):
    try:
        possibility_4Ele = Statics[hanzi1][hanzi2][hanzi3][hanzi4] / Statics[hanzi1][hanzi2][hanzi3]['total']
    except KeyError:
        possibility_4Ele = 0
    except TypeError as e:
        print(e)
    return possibility_4Ele

def getPossibilityAfterSmoothed(hanzi, p_2Ele, p_3Ele = 0, p_4Ele = 0):
    try:
        p_hanzi = possibilityOfHanzi[hanzi]
    except KeyError:
        p_hanzi = 0
    possibilityAfterSmoothed = _lambda * p_2Ele + (1 - _lambda) * p_hanzi + _miu * p_3Ele + _phi * p_4Ele
    return possibilityAfterSmoothed

def getDistance(lastNode, hanzi, eleNum):
    if eleNum == 2:
        hanzi1 = lastNode.hanzi
        hanzi2 = hanzi
        possibility_2Ele = getPossibility_2Ele(hanzi1,hanzi2)
        possibilityAfterSmoothed = getPossibilityAfterSmoothed(hanzi2,possibility_2Ele)
    elif eleNum == 3:
        llNode = lastNode.parent
        if llNode == root:
            getDistance(lastNode, hanzi, 2)
        hanzi1 = llNode.hanzi
        hanzi2 = lastNode.hanzi
        hanzi3 = hanzi
        possibility_2Ele = getPossibility_2Ele(hanzi2,hanzi3)
        possibility_3Ele = getPossibility_3Ele(hanzi1,hanzi2,hanzi3)
        possibilityAfterSmoothed = getPossibilityAfterSmoothed(hanzi3,possibility_2Ele,possibility_3Ele)
    elif eleNum == 4:
        llNode = lastNode.parent
        lllNode = llNode.parent
        if llNode == root or lllNode == root:
            return getDistance(lastNode, hanzi, 3)
        hanzi1 = lllNode.hanzi
        hanzi2 = llNode.hanzi
        hanzi3 = lastNode.hanzi
        hanzi4 = hanzi
        possibility_2Ele = getPossibility_2Ele(hanzi3,hanzi4)
        possibility_3Ele = getPossibility_3Ele(hanzi2,hanzi3,hanzi4)
        possibility_4Ele = getPossibility_4Ele(hanzi1,hanzi2,hanzi3,hanzi4)
        possibilityAfterSmoothed = getPossibilityAfterSmoothed(hanzi4,possibility_2Ele,possibility_3Ele,possibility_4Ele)
    try:
        dis = math.log(possibilityAfterSmoothed) * (-1)
    except ValueError:
        dis = 0xffffffff
    return dis

def standardizePinyin(pinyin):
    return pinyin.lower()


def compare():
    osString = 'python ./compare.py'
    f = os.popen(osString, 'r')
    res = f.readlines()
    f.close()
    wordCorrectRate = re.search(r'0.\d+',res[0]).group(0)
    sentenceCorrectRate = re.search(r'0.\d+',res[1]).group(0)
    workSheet.append([_lambda,_miu,_phi,wordCorrectRate,sentenceCorrectRate])
    print('字正确率： '+ wordCorrectRate + ', 句正确率： ' + sentenceCorrectRate)

def getDistance_1stLayer(hanzi):
    try:
        possibility = Statics[hanzi]['begin'] / totalNum_begin
    except KeyError:
        possibility = 0
    try:
        possibilityAfterSmoothed = _lambda * possibility + (1 - _lambda) * possibilityOfHanzi[hanzi]
    except KeyError:
        return 0xffffffff
    dis = math.log(possibilityAfterSmoothed) * (-1)
    return dis


def getDistance_lastLayer(hanzi):
    try:
        possibility = Statics[hanzi]['end'] / totalNum_end
    except KeyError:
        possibility = 0
    try:
        possibilityAfterSmoothed = _lambda * possibility + (1 - _lambda) * possibilityOfHanzi[hanzi]
    except KeyError:
        return 0xffffffff
    dis = math.log(possibilityAfterSmoothed) * (-1)
    return dis


def viterbi():
    t1 = time.process_time()
    print('begin viterbi...')
    outputTarget = open(OutputFile, 'w', encoding='utf-8')
    testOutput = ''
    for line in open(InputFile, 'r+', encoding='utf-8'):
        # 它对应output.txt中的一行输出，我们用viterbi算法去找出这个输出的最优解
        sList_raw = re.split(r'\s+', line.strip())  # 用空格作分割，得到s
        sList = [standardizePinyin(s) for s in sList_raw]
        depth = len(sList)
        # s所对应的汉字已由Pinyin2Hanzi所明确，接下来是viterbi算法
        nodeLayers = []
        lastLayer = []
        #print(sList)
        for hanzi in Pinyin2Hanzi[sList[0]]:
            lastLayer.append(node(hanzi, root, getDistance_1stLayer(hanzi)))
        nodeLayers.append(lastLayer)
        for nd in lastLayer:
            testOutput += 'firstLayer: ' + nd.hanzi + ' : ' + str(nd.minDistance) + '\n'
        for i in range(1, depth):
            curLayer = []
            for curHanzi in Pinyin2Hanzi[sList[i]]:
                # 寻找起点到该点的最佳路径值
                minDis = lastLayer[0].minDistance + getDistance(lastLayer[0], curHanzi, eleNum)
                tmpParent = lastLayer[0]
                for prevNode in lastLayer:  # 不断尝试进行更新，以寻找最短的距离，并且保存父节点
                    curDis = prevNode.minDistance + getDistance(prevNode, curHanzi, eleNum)
                    if curDis < minDis:
                        minDis = curDis
                        tmpParent = prevNode
                curLayer.append(node(curHanzi, tmpParent, minDis))
            #    for nd in curLayer:
            #        testOutput += nd.parent.hanzi + nd.hanzi + ' : ' + str(nd.minDistance) + '\n'
            #   testOutput += '\n---------\n'
            nodeLayers.append(curLayer)
            lastLayer = curLayer
        # 至此，所有层遍历完毕
        nd = min(nodeLayers[-1], key=lambda hanzi: hanzi.minDistance + getDistance_lastLayer(hanzi))
        output = []
        while nd.parent is not None:
            output.append(nd.hanzi)
            nd = nd.parent
        output = list(reversed(output))
        outputString = ''
        for eachWord in output:
            outputString += str(eachWord)
        # outputTarget.write(testOutput + '\n')
        outputTarget.write(outputString + '\n')
        #print(output)
    print('viterbi using ' + str(time.process_time() - t1) + ' sec.')
    print('using lambda as ' + str(_lambda) + ', miu as ' + str(_miu) + ', phi as ' + str(_phi))
    #compare()


if __name__ == '__main__':
    with open(Pinyin2HanziFile, 'r+', encoding='utf-8') as f:
        Pinyin2Hanzi = json.load(f)
        # 首先读取input.txt中的拼音

    while True:
        eleNum = int(input("请输入一个数字，代表将要使用基于字的__元模型作处理："))
        if 2 <= eleNum <= 4:
            StaticsFile += str(eleNum) + 'Ele.txt'
            break
        else:
            print('Invalid input')

    print('loading staticsFile...')
    t0 = time.process_time()
    with open(StaticsFile, 'r+', encoding='utf-8') as f:
        Statics = json.load(f)
        for eachHanzi in Statics:
            totalNum += Statics[eachHanzi]['total']
            try:
                totalNum_begin += Statics[eachHanzi]['begin']
            except KeyError:
                pass
            try:
                totalNum_end += Statics[eachHanzi]['end']
            except KeyError:
                pass
        for eachHanzi in Statics:
            possibilityOfHanzi[eachHanzi] = Statics[eachHanzi]['total'] / totalNum
    print('finishLoading, using ' + str(time.process_time() - t0) + ' sec.')

    workSheet.append(['_lambda','_miu','_phi','字正确率','句正确率'])

    if eleNum == 2:
        for _l in lambdaTable:
            _lambda = _l
            viterbi()
    elif eleNum == 3:
        for _l in lambdaTable:
            for _m in miuTable:
                _lambda = _l
                _miu = _m
                viterbi()
    elif eleNum == 4:
        for _l in lambdaTable:
            for _m in miuTable:
                for _p in phiTable:
                    _lambda = _l
                    _miu = _m
                    _phi = _p
                    viterbi()

    #wb.save('result.xlsx')