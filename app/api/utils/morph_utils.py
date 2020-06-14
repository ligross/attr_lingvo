from nltk.tokenize import word_tokenize
import itertools
import pymorphy2

MORPH_ANALYZER = pymorphy2.MorphAnalyzer()


def parse_word_morph(word):
    return MORPH_ANALYZER.parse(word)[0]


def parse_sentence_morph(sentence):
    parsed_sentence = []
    ll = [[word_tokenize(w), ' '] for w in sentence.split()]
    for word in list(itertools.chain(*list(itertools.chain(*ll)))):
        if word in ' "#$%&()*+.!?«»,\'-/:;<=>@[]^_`{|}~':
            parsed_sentence.append(word)
        else:
            parsed_sentence.append((word, parse_word_morph(word)))
    return parsed_sentence


class MorphRegexConverter:
    def __init__(self, pos):
        self.pos = pos

    def convert(self, sentence):
        converted_sentence = ''
        for word in sentence:
            if type(word) is str:
                converted_sentence += word
            else:
                parsed_word = word[1]
                if self.pos and parsed_word.tag.POS in self.pos:
                    converted_sentence += parsed_word.tag.POS
                else:
                    converted_sentence += word[0]
        return converted_sentence
