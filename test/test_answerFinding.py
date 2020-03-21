from unittest import TestCase

from answer_start.answer_finding import AnswerFinding


class TestAnswerFinding(TestCase):
    def test_find_answer_in_context(self):
        answer_text = 'eine Kupferstatue von Christus'
        context = 'Architektonisch hat die Schule einen katholischen Charakter. Über der goldenen Kuppel des ' \
                  'Hauptgebäudes befindet sich eine goldene Statue der Jungfrau Maria. Unmittelbar vor dem ' \
                  'Hauptgebäude und gegenüber befindet sich eine kupferne Christusstatue mit Waffen, die mit der ' \
                  'Legende "Venite Ad Me Omnes" emporgehoben sind.'
        result = AnswerFinding().find_answer_in_context(answer_text, context)

        self.assertEqual(result[0], 214)
        self.assertEqual(result[2], 'sich eine kupferne Christusstatue')

