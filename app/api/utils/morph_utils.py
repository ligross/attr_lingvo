import itertools

import nltk
import pymorphy2
from nltk.data import load
from nltk.tokenize import word_tokenize

from app.api.rules.rules import SENTENCES_SPLIT_REGEX, ADDITIONAL_ABBREVIATIONS, SENTENCES_SPLIT_ADD_REGEX

PUNCTUATION = ' "#$%&()*+.!?«»,\'-/:;<=>@[]^_`{|}~—'
MORPH_ANALYZER = pymorphy2.MorphAnalyzer()
TAG = MORPH_ANALYZER.TagClass

nltk.download('punkt')

TOKENIZER = load("tokenizers/punkt/{0}.pickle".format('russian'))
TOKENIZER._params.abbrev_types.update(ADDITIONAL_ABBREVIATIONS)


def tokenize_sentences(text):
    return TOKENIZER.tokenize(text)


def tokenize_corp_sentences(text):
    raw_sentences = TOKENIZER.tokenize(text)
    sentences = []
    for raw_sentence in raw_sentences:
        new_sentences = SENTENCES_SPLIT_REGEX.split(raw_sentence)
        skip_next = False
        for ind, new_sentence in enumerate(new_sentences):
            #sentences = new_sentence.split()
            # matches = list(SENTENCES_SPLIT_ADD_REGEX.finditer(new_sentence))
            # if matches:
            #     current_pos = 0
            #     for ind, match in enumerate(matches):
            #         if ind == 0:
            #             sentences.append(new_sentence[:match.start()])
            #             current_pos = match.end() - len(match.groups())
            #         else:
            #             sentences.append(new_sentence[current_pos:match.start()])
            #             current_pos = match.end() - len(match.groups())
            #     sentences.append(new_sentence[current_pos:])
            # else:
            #     sentences.append(new_sentence)
            if skip_next:
                continue
            if new_sentence[-1] in (',',) and ind < len(new_sentences) - 1:
                sentences.append(' '.join((new_sentence, new_sentences[ind + 1])))
                skip_next = True
            elif ind < len(new_sentences) - 1 and new_sentences[ind + 1][0].islower() and new_sentence[-1] not in ',.?!':
                sentences.append(' '.join((new_sentence, new_sentences[ind + 1])))
                skip_next = True
            else:
                new_sentence = new_sentence.replace('\n', ' ')
                sentences.append(new_sentence)
    return sentences


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


def match_morph(word, tags):
    for tag in tags[0]:
        if not any((t in word.tag for t in tags[0][tag])):
            return False
    return True
