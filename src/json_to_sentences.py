'''
预处理：将json转为不含汉字之外字符的句子，并且输出到res/sentence的txt文件中
'''

import jsonlines
import os
import re

ArticleDir = '..\\preprocessing\\corpus'
OutputDir = '..\\preprocessing\\res\\sentence'

allFiles = []
for root, directories, filenames in os.walk(ArticleDir):
    for filename in filenames:
        p = os.path.join(ArticleDir, filename)
        if p.endswith('.txt'):
            allFiles.append(p)

# 对语料中所有的文件进行处理
for jsonLines in allFiles:
    res = re.search(r'.*\\([^\\]*)',jsonLines)
    outputTarget = OutputDir + '\\' + res.group(1)
    print('processing '+ res.group(1) + ' to '+ outputTarget)
    if not os.path.exists(OutputDir):
        try:
            os.mkdir(OutputDir)
        except Exception as e:
            print(e)
    mid_out = open(outputTarget, 'w', encoding='utf-8')
    with open(jsonLines, 'r+', encoding='gbk') as f:
        for jsonArticle in jsonlines.Reader(f):
            html = jsonArticle['html']
            # 获取到原文内容，之后用特殊符号将原文进行分割为句子
            sentences = re.split(
                r'\s*[,.／/;；\'"\]\[_\-\=\+\\|<>?!@#$%▲％^＾&■＆*＊()~～`｀·—＝－（）“”‘＇＇’、？！，。《》【】{}①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑰⑯⑱⑲⑳1234567890a-zA-Z：∶℃…:]\s*',
                html)
            for sentence in sentences:
                # 不予考虑
                if len(sentence) < 2:
                    continue
                mid_out.write(sentence + '\n')
