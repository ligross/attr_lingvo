from collections import OrderedDict

import nltk
from nltk.tokenize import word_tokenize
import pymorphy2

nltk.download('punkt')

VOWELS = 'ауоыиэяюёе'
MORPH_ANALYZER = pymorphy2.MorphAnalyzer()


class Text:
    def __init__(self, text, attributes):
        self.text = text
        self.attributes = attributes

        self.sentences = self.__tokenize_sentences()
        self.sentences_words = [self.__tokenize_words(sentence) for sentence in self.sentences]
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
        return [(word, MORPH_ANALYZER.parse(word)[0]) for word in words]

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
        return sum(avg_word_len) / len(self.sentences_words)

    def avg_sent_len_in_words(self):
        return self.total_words / len(self.sentences_words)

    def sentence_len8_count(self):
        """ Count of the sentences which length is more that 8 words in percents"""
        return sum((1 for sentence in self.sentences_words if len(sentence) > 8)) / len(self.sentences_words)

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
            return 0

    def qu_coefficient(self):
        try:
            return (self.total_adjectives + self.total_pronouns) / (self.total_verbs + self.total_nouns)
        except ZeroDivisionError:
            return 0

    def ac_coefficient(self):
        try:
            return (self.total_verbs + self.total_verb_forms) / self.total_words
        except ZeroDivisionError:
            return 0

    def din_coefficient(self):
        try:
            return (self.total_verbs + self.total_verb_forms) / \
                   (self.total_nouns + self.total_adjectives + self.total_pronouns)
        except ZeroDivisionError:
            return 0  # TODO is there a better way to handle this?

    def con_coefficient(self):
        return (self.total_prepositions + self.total_conjunctions) / len(self.sentences)

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
        return self.results
