from nltk.tokenize import word_tokenize
import itertools
import pymorphy2

PUNCTUATION = ' "#$%&()*+.!?«»,\'-/:;<=>@[]^_`{|}~'
MORPH_ANALYZER = pymorphy2.MorphAnalyzer()
TAG = MORPH_ANALYZER.TagClass


def parse_word_morph(word):
    return MORPH_ANALYZER.parse(word)[0]


def parse_sentence_morph(sentence):
    parsed_sentence = []
    ll = [[word_tokenize(w), ' '] for w in sentence.split()]
    for word in list(itertools.chain(*list(itertools.chain(*ll)))):
        if word in PUNCTUATION:
            parsed_sentence.append((word, None))
        else:
            parsed_sentence.append((word, parse_word_morph(word)))
    return parsed_sentence


class MorphRegexConverter:
    def __init__(self, pos=None, tags=None):
        self.pos = pos
        self.tags = tags

    def convert(self, sentence):
        converted_sentence = ''
        for word, parsed_word in sentence:
            if not parsed_word:
                converted_sentence += word
            else:
                if self.pos and parsed_word.tag.POS in self.pos:
                    converted_sentence += parsed_word.tag.POS
                else:
                    if self.tags:
                        found = False
                        for tag in self.tags:
                            if tag in parsed_word.tag:
                                found = True
                                converted_sentence += tag
                                break
                        if not found:
                            converted_sentence += word
                    else:
                        converted_sentence += word
        return converted_sentence


class ExtendedMorphRegexConverter:
    """
    pattern = {'pos': ('Noun',),
               'genus': ('m', 'f'),
               'rename_to': 'NOUN',
               'anim': ('anim',),
               'number': ('sing', 'plur'),
               'case': ('nom','gen'),
               'person': ('1p', '2p'),
               }
    """
    def __init__(self, patterns: list):
        self.patterns = patterns

    def convert(self, sentence):
        converted_sentence = ''
        for word, parsed_word in sentence:
            if not parsed_word:
                converted_sentence += word
            else:
                for pattern in self.patterns:
                    if pattern.get('pos') and parsed_word.tag.POS not in pattern['pos']:
                        converted_sentence += word
                        continue
                    if pattern.get('person') and parsed_word.tag.person not in pattern['person']:
                        converted_sentence += word
                        continue
                    if pattern.get('number') and parsed_word.tag.number not in pattern['number']:
                        converted_sentence += word
                        continue
                    converted_sentence += pattern['rename_to']
        return converted_sentence


def match_tags(sentence, tags):
    matches = 0
    for word, parsed_word in sentence:
        if not parsed_word:
            continue
        else:
            for tag in tags:
                if set(tag) in parsed_word.tag:
                    matches += 1
    return matches
