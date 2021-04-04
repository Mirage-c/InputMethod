'''
将拼音汉字表转为json，便于后续调用
'''
import os
import re
import json

Table = '..\\preprocessing\\拼音汉字表.txt'
outputTarget = '..\\preprocessing\\res\\pinyin_hanzi.txt'
dict = {}
with open(outputTarget, 'w', encoding='utf-8') as f:
    for line in open(Table, 'r+', encoding='utf-8'):
        # 每一行对应一个读音
        res = re.match(r'([a-z]+)\s(.*)',line)
        dict.setdefault(res.group(1),[])
        words = res.group(2).split(' ')
        dict[res.group(1)] = words
    json.dump(dict, f)

