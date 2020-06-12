from collections import OrderedDict

import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')


class Text:
    def __init__(self, text, attributes):
        self.text = text
        self.attributes = attributes

        self.sentences = self.__tokenize_sentences()
        self.sentences_words = [self.__tokenize_words(sentence) for sentence in self.sentences]

        self.results = OrderedDict()

    def __tokenize_sentences(self):
        return nltk.sent_tokenize(self.text, language="russian")

    def __tokenize_words(self, sentence):
        return list(filter(lambda word: word not in '"#$%&()*+.!?«»,\'-/:;<=>@[]^_`{|}~',
                           word_tokenize(sentence)))

    def avg_word_len(self):
        # array of average word lengths for each sentence
        avg_word_len = []
        for sentence in self.sentences_words:
            avg_word_len.append(sum((len(word) for word in sentence)) / len(sentence))
        return sum(avg_word_len) / len(self.sentences_words)

    def avg_sent_len_in_words(self):
        return sum((len(sentence) for sentence in self.sentences_words)) / len(self.sentences_words)

    def sentence_len8_count(self):
        """ Count of the sentences which length is more that 8 words"""
        return sum((1 for sentence in self.sentences_words if len(sentence) > 8))

    def calculate_results(self):
        if 'avg_word_len' in self.attributes.keys():
            self.results['avg_word_len'] = {'name': self.attributes['avg_word_len']['name'],
                                            'result': self.avg_word_len()}
        if 'avg_sentence_len' in self.attributes.keys():
            self.results['avg_sentence_len'] = {'name': self.attributes['avg_sentence_len']['name'],
                                                'result': self.avg_sent_len_in_words()}
        if 'sentence_len8_count' in self.attributes.keys():
            self.results['sentence_len8_count'] = {'name': self.attributes['sentence_len8_count']['name'],
                                                   'result': self.avg_sent_len_in_words()}
        return self.results