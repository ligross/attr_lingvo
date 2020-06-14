from collections import OrderedDict

from pyaspeller import YandexSpeller
from flask import current_app
import nltk
from nltk.tokenize import word_tokenize

from app.api.data.intro_words import INTRO_WORDS_REGEXP
from app.api.data.rules import *
from app.api.utils.morph_utils import parse_word_morph, parse_sentence_morph, MorphRegexConverter

nltk.download('punkt')

NAN_ELEMENT = 'N/A'
VOWELS = 'ауоыиэяюёе'
IPM_MULTIPLIER = 1000000

SPELLER = YandexSpeller(lang='ru',
                        find_repeat_words=False,
                        ignore_digits=True,
                        ignore_latin=True,
                        ignore_roman_numerals=True,
                        ignore_uppercase=True,
                        ignore_urls=True,
                        )


class Text:
    def __init__(self, text, attributes):
        self.text = text
        self.attributes = attributes

        self.sentences = self.__tokenize_sentences()
        self.sentences_words = [self.__tokenize_words(sentence) for sentence in self.sentences]
        self.morph_parsed_sentences = [parse_sentence_morph(sentence) for sentence in self.sentences]
        self.total_words = sum((len(sentence) for sentence in self.sentences_words))
        self.total_syllables, self.total_complex_words = self.__count_total_syllables()

        self.total_nouns = 0
        self.total_pronouns = 0
        self.total_adjectives = 0
        self.total_verbs = 0
        self.total_verb_forms = 0
        self.total_adverbs = 0
        self.total_prepositions = 0
        self.total_conjunctions = 0

        self.__calculate_total_speech_parts()

        self.results = OrderedDict()

    def __tokenize_sentences(self):
        return nltk.sent_tokenize(self.text, language="russian")

    @staticmethod
    def __tokenize_words(sentence):
        words = filter(lambda w: w not in '"#$%&()*+.!?«»,\'-/:;<=>@[]^_`{|}~',
                       word_tokenize(sentence))
        return [(word, parse_word_morph(word)) for word in words]

    def __calculate_total_speech_parts(self):
        for sentence in self.sentences_words:
            for word, parsed_word in sentence:
                tag = str(parsed_word.tag.POS)
                if tag in ('NOUN',):
                    self.total_nouns += 1
                elif tag in ('NPRO',):
                    self.total_pronouns += 1
                elif tag in ('ADJF', 'ADJS'):
                    self.total_adjectives += 1
                elif tag in ('VERB', 'INFN'):
                    self.total_verbs += 1
                elif tag in ('ADVB',):
                    self.total_adverbs += 1
                elif tag in ('PRTF', 'PRTS', 'GRND'):
                    self.total_verb_forms += 1
                elif tag in ('PREP',):
                    self.total_prepositions += 1
                elif tag in ('CONJ',):
                    self.total_conjunctions += 1

    def __count_total_syllables(self):
        total_syllables = 0
        total_complex_words = 0
        for sentence in self.sentences_words:
            for word in sentence:
                word = word[0].lower()
                syllables_count = sum((1 for symbol in word if symbol in VOWELS))
                if syllables_count >= 3:
                    total_complex_words += 1
                total_syllables += syllables_count
        return total_syllables, total_complex_words

    def avg_word_len(self):
        # array of average word lengths for each sentence
        avg_word_len = []
        for sentence in self.sentences_words:
            avg_word_len.append(sum((len(word[0]) for word in sentence)) / len(sentence))
        return sum(avg_word_len) / len(self.sentences)

    def avg_sent_len_in_words(self):
        return self.total_words / len(self.sentences)

    def sentence_len8_count(self):
        """ Count of the sentences which length is more that 8 words in percents"""
        return (sum((1 for sentence in self.sentences_words if len(sentence) > 8)) / len(
            self.sentences)) * IPM_MULTIPLIER

    def flesch_kincaid_index(self):
        """ The Flesch–Kincaid readability tests are readability tests designed to indicate
         how difficult a passage in English is to understand """

        return 0.39 * (self.total_words / len(self.sentences)) + 11.8 * (
                self.total_syllables / self.total_words) - 15.59

    def fog_index(self):
        """ The Gunning fog index is a readability test.
         The index estimates the years of formal education a person needs to understand the text on the first reading """
        return 0.4 * (0.78 * self.avg_sent_len_in_words() + 100 * (self.total_complex_words / self.total_words))

    def pr_coefficient(self):
        try:
            return (self.total_nouns + self.total_pronouns) / (self.total_adjectives + self.total_verbs)
        except ZeroDivisionError:
            return NAN_ELEMENT

    def qu_coefficient(self):
        try:
            return (self.total_adjectives + self.total_pronouns) / (self.total_verbs + self.total_nouns)
        except ZeroDivisionError:
            return NAN_ELEMENT

    def ac_coefficient(self):
        try:
            return (self.total_verbs + self.total_verb_forms) / self.total_words
        except ZeroDivisionError:
            return NAN_ELEMENT

    def din_coefficient(self):
        try:
            return (self.total_verbs + self.total_verb_forms) / \
                   (self.total_nouns + self.total_adjectives + self.total_pronouns)
        except ZeroDivisionError:
            return NAN_ELEMENT

    def con_coefficient(self):
        return (self.total_prepositions + self.total_conjunctions) / len(self.sentences)

    def get_errors(self):
        try:
            errors = list(SPELLER.spell(self.text))
            current_app.logger.info(f'Found errors: {errors}')
            return (len(errors) / self.total_words) * IPM_MULTIPLIER
        except Exception as ex:
            current_app.logger.error(f'Exceptions trying to get/parse errors: {ex}')
            return NAN_ELEMENT

    def uniform_rows_count(self):
        """ IPM of sentences with uniform rows"""
        for sentence in self.sentences_words:
            for word in sentence:
                # tag = str(parsed_word.tag.POS)
                pass
        return NAN_ELEMENT

    def introductory_words_count(self):
        introductory_words_count = 0
        for sentence in self.sentences:
            matches = INTRO_WORDS_REGEXP.findall(sentence)
            introductory_words_count += len(matches)
        return (introductory_words_count / self.total_words) * IPM_MULTIPLIER

    def comparatives_count(self):
        comparatives_count = 0
        converter = MorphRegexConverter(pos=('INFN',))
        for parsed_sentence, sentence in zip(self.morph_parsed_sentences, self.sentences):
            pos_matches = COMPARATIVES_REGEX_POS.findall(converter.convert(sentence=parsed_sentence))
            matches = COMPARATIVES_REGEX.findall(sentence)
            comparatives_count += len(pos_matches) + len(matches)

        return (comparatives_count / self.total_words) * IPM_MULTIPLIER

    def syntax_splices_count(self):
        syntax_splices_count = 0
        converter = MorphRegexConverter(pos=('VERB',))
        for parsed_sentence, sentence in zip(self.morph_parsed_sentences, self.sentences):
            pos_matches = SYNTAX_SPLICES_REGEX_POS.findall(converter.convert(sentence=parsed_sentence))
            matches = SYNTAX_SPLICES_REGEX.findall(sentence)
            syntax_splices_count += len(pos_matches) + len(matches)
        return (syntax_splices_count / self.total_words) * IPM_MULTIPLIER

    def comparative_clauses_count(self):
        comparative_clauses_count = 0
        for sentence in self.sentences:
            matches = COMPARATIVE_CLAUSES_REGEX.findall(sentence)
            comparative_clauses_count += len(matches)
        return (comparative_clauses_count / self.total_words) * IPM_MULTIPLIER

    def calculate_results(self):
        if 'flesch_kincaid_index' in self.attributes.keys():
            self.results['flesch_kincaid_index'] = {'name': self.attributes['flesch_kincaid_index']['name'],
                                                    'result': self.flesch_kincaid_index()}
        if 'fog_index' in self.attributes.keys():
            self.results['fog_index'] = {'name': self.attributes['fog_index']['name'],
                                         'result': self.fog_index()}
        if 'avg_word_len' in self.attributes.keys():
            self.results['avg_word_len'] = {'name': self.attributes['avg_word_len']['name'],
                                            'result': self.avg_word_len()}
        if 'avg_sentence_len' in self.attributes.keys():
            self.results['avg_sentence_len'] = {'name': self.attributes['avg_sentence_len']['name'],
                                                'result': self.avg_sent_len_in_words()}
        if 'sentence_len8_count' in self.attributes.keys():
            self.results['sentence_len8_count'] = {'name': self.attributes['sentence_len8_count']['name'],
                                                   'result': self.sentence_len8_count()}
        if 'pr_coefficient' in self.attributes.keys():
            self.results['pr_coefficient'] = {'name': self.attributes['pr_coefficient']['name'],
                                              'result': self.pr_coefficient()}
        if 'qu_coefficient' in self.attributes.keys():
            self.results['qu_coefficient'] = {'name': self.attributes['qu_coefficient']['name'],
                                              'result': self.qu_coefficient()}
        if 'ac_coefficient' in self.attributes.keys():
            self.results['ac_coefficient'] = {'name': self.attributes['ac_coefficient']['name'],
                                              'result': self.ac_coefficient()}
        if 'din_coefficient' in self.attributes.keys():
            self.results['din_coefficient'] = {'name': self.attributes['din_coefficient']['name'],
                                               'result': self.din_coefficient()}
        if 'con_coefficient' in self.attributes.keys():
            self.results['con_coefficient'] = {'name': self.attributes['con_coefficient']['name'],
                                               'result': self.con_coefficient()}
        if 'errors' in self.attributes.keys():
            self.results['errors'] = {'name': self.attributes['errors']['name'],
                                      'result': self.get_errors()}
        if 'uniform_rows_count' in self.attributes.keys():
            self.results['uniform_rows_count'] = {'name': self.attributes['uniform_rows_count']['name'],
                                                  'result': self.uniform_rows_count()}
        if 'introductory_words_count' in self.attributes.keys():
            self.results['introductory_words_count'] = {'name': self.attributes['introductory_words_count']['name'],
                                                        'result': self.introductory_words_count()}
        if 'comparatives_count' in self.attributes.keys():
            self.results['comparatives_count'] = {'name': self.attributes['comparatives_count']['name'],
                                                  'result': self.comparatives_count()}
        if 'syntax_splices_count' in self.attributes.keys():
            self.results['syntax_splices_count'] = {'name': self.attributes['syntax_splices_count']['name'],
                                                    'result': self.syntax_splices_count()}
        if 'comparative_clauses_count' in self.attributes.keys():
            self.results['comparative_clauses_count'] = {'name': self.attributes['comparative_clauses_count']['name'],
                                                         'result': self.comparative_clauses_count()}
        return self.results
