from unittest import TestCase
from sentence_tokenizer import SentenceTokenizer


class TestSentenceTokenizer(TestCase):

    def test_sentenize_text(self):
        tokenizer = SentenceTokenizer()
        result_en = tokenizer.sentenize_text('The first sentence. The second sentence.')
        result_de = tokenizer.sentenize_text('Das ist der erste Satz. Das ist der zweite Satz.')

        self.assertEqual(len(result_en), 2)
        self.assertEqual(len(result_de), 2)
