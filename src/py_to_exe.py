'''
将.py转换为.exe
运行：python py_to_exe.py py2exe
'''

from distutils.core import setup
import py2exe

setup(console=['pinyin.py'])