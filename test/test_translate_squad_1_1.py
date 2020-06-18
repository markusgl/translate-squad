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
        squad_translation = SquadTranslation()
        answer_start = 70
        result = squad_translation.find_sentence_number(answer_start, self.context_de)
        self.assertEqual(result, 1)

    def test_find_sentence_number_bad_case(self):
        squad_translation = SquadTranslation()
        answer_start = 400
        result = squad_translation.find_sentence_number(answer_start, self.context_de)
        self.assertEqual(result, None)

    def test_search_answer_in_translated_context(self):
        squad_translation = SquadTranslation()
        squad_translation.search_answer_in_translated_context()

    def test_iterate_qas(self):
        squad_translation = SquadTranslation()
        paragraph = {
          "context": "Architecturally, the school has a Catholic character. Atop the Main Building's gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend \"Venite Ad Me Omnes\". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.",
          "qas": [
            {
              "answers": [
                {
                  "answer_start": 515,
                  "text": "Saint Bernadette Soubirous"
                }
              ],
              "question": "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?",
              "id": "5733be284776f41900661182"
            }
          ]
        }
        result = squad_translation.iterate_qas(orig_context=self.context_en, paragraph=paragraph, translated_context=self.context_de)
        print(result)
        self.assertEquals(result, paragraph['qas'])

    def test_iterate_answers(self):
        squad_translation = SquadTranslation()
        result = squad_translation.iterate_answers(answers=self.translated_answer, orig_context=self.context_en,
                                                   translated_context=self.context_de)

        self.assertEquals(result, [{'answer_start': 214, 'text': 'sich eine kupferne Christusstatue'}])
