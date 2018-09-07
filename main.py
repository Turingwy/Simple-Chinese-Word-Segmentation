from tuwords.word_segment import Segmenter
import random


"""
获得交叉验证的索引
"""
def get_cross_valid(sample_len, count):
    cross_valid_index = list(range(0, sample_len))
    random.shuffle(cross_valid_index)
    per_count = sample_len // count
    for i in range(count-1):
        valid_index = cross_valid_index[per_count*i: per_count*(i+1)]
        train_index = cross_valid_index[0: per_count*i]
        train_index += cross_valid_index[per_count*(i+1):]
        yield train_index, valid_index
    yield cross_valid_index[0: per_count*(count-1)], cross_valid_index[per_count*(count-1):]

def get_word_freq_dict(sentences):
    word_freq_dict = {}
    for s in sentences:
        for word in s:
            word_freq_dict[word] = word_freq_dict.get(word, 0) + 1
    return word_freq_dict

def get_correct_count(valid_sentences, segmenter_sentences):
    corrent_count = 0
    valid_word_count = 0
    segmenter_word_count = 0
    for valid_sent, segmenter_sent in zip(valid_sentences, segmenter_sentences):
        ind1 = 0
        ind2 = 0
        last_offset = 0

        valid_word_count += len(valid_sent)
        segmenter_word_count += len(segmenter_sent)

        while ind1 < len(valid_sent) and ind2 < len(segmenter_sent):
            if len(valid_sent[ind1]) - last_offset == len(segmenter_sent[ind2]):
                ind1 += 1
                ind2 += 1
                if last_offset == 0:
                    corrent_count += 1
                else:
                    last_offset = 0

            else:
                last = 0
                if ind1 < len(valid_sent) and ind2 < len(segmenter_sent) \
                        and len(valid_sent[ind1]) - last_offset < len(segmenter_sent[ind2]) - last:
                    while ind1 < len(valid_sent) and ind2 < len(segmenter_sent) \
                            and len(valid_sent[ind1]) - last_offset < len(segmenter_sent[ind2]) - last:
                        last += len(valid_sent[ind1]) - last_offset
                        last_offset = 0
                        ind1 += 1

                    last_offset = len(segmenter_sent[ind2]) - last
                    ind2 += 1

                if ind1 < len(valid_sent) and ind2 < len(segmenter_sent) \
                        and len(valid_sent[ind1]) - last_offset > len(segmenter_sent[ind2]):
                    last_offset += len(segmenter_sent[ind2])
                    ind2 += 1

    return corrent_count, valid_word_count, segmenter_word_count


if __name__ == '__main__':
    # 读入所有文本, 转化为句子
    sentences = []
    with open("newtrain.txt") as f:
        current_sentence = []
        for ind, line in enumerate(f):
            if line[:-1] == "EOS":
                sentences.append(current_sentence)
                current_sentence = []

            item = line.split()

            if len(item) <= 1 or item[1][0] in ("W", "K", "L"):
                continue

            current_sentence.append(item[0])

    for train_index, valid_index in get_cross_valid(len(sentences), 5):
        train_sentences = []
        for ind in train_index:
            train_sentences.append(sentences[ind])

        word_freq_dict = get_word_freq_dict(train_sentences)
        segmenter = Segmenter(word_freq_dict)
        valid_sentences = []
        segmenter_sentences = []
        for ind in valid_index:
            valid_sentence = ''.join(sentences[ind])
            valid_sentences.append(sentences[ind])
            segmenter_sentences.append(list(segmenter.cut(valid_sentence)))

        corrent_count, valid_count, segmenter_count = get_correct_count(valid_sentences, segmenter_sentences)
        p = corrent_count / segmenter_count
        r = corrent_count / valid_count
        print("precision: %f" % (p))
        print("recall: %f" % (r))
        print('F1: %f' % ((2 * p * r) / (p + r)))
        print()



















