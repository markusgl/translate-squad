from unittest import TestCase

from answer_start.answer_finder import AnswerFinder


class TestAnswerFinding(TestCase):
    def test_find_answer_in_context(self):
        answer_text = 'eine Kupferstatue von Christus'
        context = 'Architektonisch hat die Schule einen katholischen Charakter. Über der goldenen Kuppel des ' \
                  'Hauptgebäudes befindet sich eine goldene Statue der Jungfrau Maria. Unmittelbar vor dem ' \
                  'Hauptgebäude und gegenüber befindet sich eine kupferne Christusstatue mit Waffen, die mit der ' \
                  'Legende "Venite Ad Me Omnes" emporgehoben sind.'
        ae = AnswerFinder()

        char_to_word_offsett, p_result, substring = ae.find_most_common_substring(answer_text, context)

        self.assertEqual(char_to_word_offsett, 214)
        self.assertGreater(p_result, 0.7)
        self.assertEqual(substring, 'sich eine kupferne Christusstatue')

    def test_find_answer_in_context_exact_match(self):
        substring = 'goldene Statue der Jungfrau Maria'
        context = 'Architektonisch hat die Schule einen katholischen Charakter. Über der goldenen Kuppel des ' \
                  'Hauptgebäudes befindet sich eine goldene Statue der Jungfrau Maria. Unmittelbar vor dem ' \
                  'Hauptgebäude und gegenüber befindet sich eine kupferne Christusstatue mit Waffen, die mit der ' \
                  'Legende "Venite Ad Me Omnes" emporgehoben sind.'
        ae = AnswerFinder()

        char_to_word_offsett, p_result, substring = ae.find_most_common_substring(substring, context)

        self.assertEqual(char_to_word_offsett, 123)
        self.assertEqual(p_result, 1.00)
        self.assertEqual(substring, substring)
