import os
import re

DICT_PATH = os.path.normpath(os.path.join(os.getcwd(), "../dict.txt"))
CH_RE = re.compile(r'([\u4E00-\u9FA5a-zA-Z0-9]*)([\s+\.\!\/_,$%^*(+\"\'+——！，。？、~@#￥%……&*（）]*)')
EN_RE = re.compile(r'([\u4E00-\u9FA5]*)([a-zA-Z0-9]*)')