from typing import Text

from .flair_embeddings import FlairEmbeddingModels
from nltk.tokenize import word_tokenize


class AnswerFinder:
    def __init__(self):
        self.fem = FlairEmbeddingModels().de_lang()

    def find_answer_in_context(self, answer_text: Text, context: Text):
        """
        Finds a string inside a context using word embeddings
        :param answer_text:
        :param context:
        :return:
        """
        tokenized_answer = word_tokenize(answer_text)
        tokenized_context = word_tokenize(context)

        window_size = len(tokenized_answer)
        context_range = len(tokenized_context) - window_size

        p_result = 0.0
        p_words = [""]

        # sliding window approach
        for i in range(context_range):
            current_window = tokenized_context[i:i + window_size]
            current_result = self.fem.n_similarity(current_window, tokenized_answer)

            if current_result > p_result:
                p_result = current_result
                p_words = current_window

        substring = ""
        for word in p_words:
            substring += word + " "
        substring = substring.rstrip()

        char_to_word_offset = context.find(substring)

        return char_to_word_offset, p_result, substring

