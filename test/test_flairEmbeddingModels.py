from unittest import TestCase

from answer_start.flair_embeddings import FlairEmbeddingModels


class TestFlairEmbeddingModels(TestCase):

    def test_get_word_embeddings(self):
        fem = FlairEmbeddingModels().de_lang()
        multi_word_result = fem.get_word_embeddings('a statue of christ', True)
        single_word_result = fem.get_word_embeddings('statue', True)

        self.assertEqual(len(multi_word_result), len(single_word_result))

    def test_n_similarity(self):
        fem = FlairEmbeddingModels().de_lang()
        similar_result = fem.n_similarity(['this is a test'], ['this is a test'])
        not_similar_result = fem.n_similarity(['this is a test'], ['i am a teapot'])

        self.assertEqual(similar_result, 1.0)
        self.assertLess(not_similar_result, 0.7)
