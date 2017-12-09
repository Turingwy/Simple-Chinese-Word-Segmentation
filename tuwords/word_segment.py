from tuwords.constants import *
from sys import float_info
from math import log
import re

class Segmenter:
    def __init__(self, dict_path=DICT_PATH):
        self.dict_path = dict_path
        self.prefix_freqs, self.total_freq = self.__read_dict()

    def __read_dict(self):
        freqs = {}
        total_freq = 0
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            for line in f:
                word, fq = line.split(' ')[:2]
                freqs[word] = int(fq)
                total_freq += int(fq)
                for k in range(1, len(word)):
                    if word[:k] not in freqs:
                        freqs[word[:k]] = 0

        return freqs, total_freq

    def __get_DAG(self, sentence):
        dag = [0]*len(sentence)
        for k in range(len(sentence)):
            dag[k] = []
            for j in range(k+1, len(sentence)):
                if sentence[k:j+1] not in self.prefix_freqs:
                    break

                if self.prefix_freqs[sentence[k:j+1]]:
                    dag[k].append(j)

            if not dag[k]:
                dag[k] = [k]
        return dag

    def __get_max_prob(self, dag, sentence):
        start = len(sentence) - 1
        path = [-1]*(len(sentence)+1)
        probs = [-float_info[0]]*(len(sentence)+1)
        probs[len(sentence)] = 0
        while start >= 0:
            for end in dag[start]:
                curr_prob = log(self.prefix_freqs[sentence[start:end+1]]) - log(self.total_freq) + probs[end+1]
                if curr_prob > probs[start]:
                    probs[start] = curr_prob
                    path[start] = end
            start -= 1
        return path

    def cut(self, sentence, cut_all=False):
        for block in self.__cut_blocks(sentence):
            word_dag = self.__get_DAG(block[0])
            if cut_all:
                for start, ends in enumerate(word_dag):
                    for end in ends:
                        yield block[0][start:end+1]
            else:
                path = self.__get_max_prob(word_dag, block[0])
                curr = 0
                while path[curr] >= 0:
                    yield block[0][curr:path[curr]+1]
                    curr = path[curr] + 1
            yield block[1]

    def __cut_blocks(self, sentence):
        ch_blocks = re.findall(CH_RE, sentence)
        real_blocks = []
        for bl in ch_blocks:
            real_blocks.extend([[x[0], x[1]] for x in re.findall(EN_RE, bl[0])[:-1]])
            real_blocks[-1][1] = bl[1]
        print(real_blocks)
        return real_blocks


print(list(Segmenter().cut("近日，党委常委、副校长毕明树在主楼312会议室会见了来访我校的日本名古屋大学财满镇明副校长一行。国际合作与交流处、科学技术研究院、技术研究开发院相关负责人陪同会见。")))
