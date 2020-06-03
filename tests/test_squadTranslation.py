from unittest import TestCase
from translate_squad_1_1 import SquadTranslation


class TestSquadTranslation(TestCase):
    def test_find_sentence_number(self):
        context = 'Architektonisch hat die Schule einen katholischen Charakter. Über der goldenen Kuppel des ' \
                  'Hauptgebäudes befindet sich eine goldene Statue der Jungfrau Maria. Unmittelbar vor dem ' \
                  'Hauptgebäude und gegenüber befindet sich eine kupferne Christusstatue mit Waffen, die mit der ' \
                  'Legende "Venite Ad Me Omnes" emporgehoben sind.'
        answer_start = 70
        squad_translation = SquadTranslation()
        result = squad_translation.find_sentence_number(answer_start, context)
        self.assertEqual(result, 1)

    def test_translate_squad_dataset(self):
        squad_translation = SquadTranslation()
        squad_translation.translate_squad_dataset('data/train-v1.1_mock.json', 'data/translated', character_limit=1000)
