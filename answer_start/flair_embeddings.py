"""
Flair embeddings(https://github.com/zalandoresearch/flair/blob/master/resources/docs/TUTORIAL_3_WORD_EMBEDDING.md)
"""

import re
import warnings
from typing import Text, Optional, List

warnings.filterwarnings("ignore")

from flair.data import Sentence
from flair.embeddings import WordEmbeddings, BertEmbeddings
from torch import nn


class FlairEmbeddingModels:
    def __init__(self, embeddings=None):
        self.embeddings = embeddings
        self.flair_embeddings = {}
        warnings.filterwarnings("ignore")

    """ **** Factory methods  **** """
    @classmethod
    def de_lang(cls):
        """ German FastText embeddings """
        return cls(WordEmbeddings('de'))

    @classmethod
    def de_lang_crawls(cls):
        """ German FastText embeddings trained over crawls """
        return cls(WordEmbeddings('de-crawl'))

    @classmethod
    def multilingual(cls):
        """ Multilingual BERT embeddings """
        return cls(BertEmbeddings('bert-base-multilingual-cased'))

    @classmethod
    def en_lang(cls):
        """ English FastText embeddings """
        return cls(WordEmbeddings('en-glove'))

    @classmethod
    def en_lang_crawls(cls):
        """ English FastText embeddings trained over crawls """
        return cls(WordEmbeddings('en-crawl'))

    def get_word_embeddings(self, text: Text, clean: Optional[bool] = False):
        """
        Returns the glove word embedding representation of one or multiple words.
        If multiple words are given, it sums up the word embeddings of each word.
        :param text: text as string
        :param clean: use a RegEx to remove two ore more consecutive white spaces
        :return: sum of word embeddings inside text
        """
        if clean:
            text = re.sub(r'\s{2,}', ' ', text)

        sentence = Sentence(text)
        self.embeddings.embed(sentence)

        words_embeddings = []
        for token in sentence:
            words_embeddings.append(token.embedding)

        return sum(words_embeddings)

    def n_similarity(self, words1: List, words2: List):
        """
        Returns cosine similarity between words1 and words2 as a float (i.e. '100.0' means identical)
        :param words2: array of words as strings
        :param words1: array of words as strings
        :return: cosine similarity between the two word arrays
        """
        if type(words1) == list:
            text1 = ''
            for word in words1:
                text1 += word + ' '
        else:
            text1 = words1

        if type(words2) == list:
            text2 = ''
            for word in words2:
                text2 += word + ' '
        else:
            text2 = words2

        words1_embeddings = self.get_word_embeddings(text1)
        words2_embeddings = self.get_word_embeddings(text2)

        # measure cosine similarity between both embedding summaries (tensors)
        cos = nn.CosineSimilarity(dim=0)
        result = cos(words1_embeddings, words2_embeddings)

        return result
