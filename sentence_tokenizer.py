import logging

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.corpus import gutenberg


class SentenceTokenizer:
    def __init__(self):
        self.abbreviations = ['geb', 'dr', 'z.B.', 'd.h.']
        self.tokenizer = None
        self.train_tokenizer()

    def train_tokenizer(self):
        logging.info('Training custom sentence tokenizer...')
        #nltk.download('gutenberg')

        text = ""
        for file_id in gutenberg.fileids():
            text += gutenberg.raw(file_id)

        trainer = PunktTrainer()
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.train(text)
        self.tokenizer = PunktSentenceTokenizer(trainer.get_params())

        for abbr in self.abbreviations:
            self.tokenizer._params.abbrev_types.add(abbr)

    def tokenize_sentence(self, text):
        return self.tokenizer.tokenize(text)
