from unittest import TestCase
from translate_squad_1_1 import SquadTranslation


class TestSquadTranslation(TestCase):
    def setUp(self) -> None:
        self.context_de = 'Architektonisch hat die Schule einen katholischen Charakter. Über der goldenen Kuppel des ' \
                          'Hauptgebäudes befindet sich eine goldene Statue der Jungfrau Maria. Unmittelbar vor dem ' \
                          'Hauptgebäude und gegenüber befindet sich eine kupferne Christusstatue mit Waffen, die mit ' \
                          'der Legende "Venite Ad Me Omnes" emporgehoben sind.'
        self.context_en = "Architecturally, the school has a Catholic character. Atop the Main Building's gold dome " \
                          "is a golden statue of the Virgin Mary. Immediately in front of the Main Building and " \
                          "facing it, is a copper statue of Christ with arms upraised with the legend \"Venite Ad " \
                          "Me Omnes\"."
        self.orig_answers = [{
                  "answer_start": 188,
                  "text": "a copper statue of Christ"
                }]
        self.translated_answer = [{
                  "answer_start": 188,
                  "text": "eine Kupferstatue von Christus"
                }]

    def test_find_sentence_number(self):
        answer_start = 70
        squad_translation = SquadTranslation()
        result = squad_translation.find_sentence_number(answer_start, self.context_de)
        self.assertEqual(result, 1)

    def test_translate_squad_dataset(self):
        squad_translation = SquadTranslation()
        squad_translation.translate_squad_dataset('data/train-v1.1_mock.json', 'data/translated', character_limit=1000)

    def test_iterate_answers(self):
        squad_translation = SquadTranslation()
        threshold = 0.5
        result = squad_translation.iterate_answers(answers=self.translated_answer, orig_context=self.context_en,
                                                   threshold=threshold, translated_context=self.context_de)

        self.assertEquals(result, [{'answer_start': 214, 'text': 'sich eine kupferne Christusstatue'}])
