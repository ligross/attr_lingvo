from collections import OrderedDict

import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

VOWELS = 'ауоыиэяюёе'


class Text:
    def __init__(self, text, attributes):
        self.text = text
        self.attributes = attributes

        self.sentences = self.__tokenize_sentences()
        self.sentences_words = [self.__tokenize_words(sentence) for sentence in self.sentences]
        self.total_words = sum((len(sentence) for sentence in self.sentences_words))
        self.total_syllables, self.total_complex_words = self.__count_total_syllables()

        self.results = OrderedDict()

    def __tokenize_sentences(self):
        return nltk.sent_tokenize(self.text, language="russian")

    @staticmethod
    def __tokenize_words(sentence):
        return list(filter(lambda word: word not in '"#$%&()*+.!?«»,\'-/:;<=>@[]^_`{|}~',
                           word_tokenize(sentence)))

    def __count_total_syllables(self):
        total_syllables = 0
        total_complex_words = 0
        for sentence in self.sentences_words:
            for word in sentence:
                word = word.lower()
                syllables_count = sum((1 for symbol in word if symbol in VOWELS))
                if syllables_count >= 3:
                    total_complex_words += 1
                total_syllables += syllables_count
        return total_syllables, total_complex_words

    def avg_word_len(self):
        # array of average word lengths for each sentence
        avg_word_len = []
        for sentence in self.sentences_words:
            avg_word_len.append(sum((len(word) for word in sentence)) / len(sentence))
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
        return self.results
