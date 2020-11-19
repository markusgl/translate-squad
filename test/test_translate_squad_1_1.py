import json
from unittest import TestCase, skip
from unittest.mock import MagicMock

from translate_squad_1_1 import SquadTranslation


class TestSquadTranslation(TestCase):
    def setUp(self) -> None:
        self.orig_context = "Architecturally, the school has a Catholic character. Atop the Main Building's gold dome " \
                            "is a golden statue of the Virgin Mary. Immediately in front of the Main Building and " \
                            "facing it, is a copper statue of Christ with arms upraised with the legend \"Venite Ad " \
                            "Me Omnes\"."
        self.translated_context = 'Architektonisch hat die Schule einen katholischen Charakter. Über der goldenen ' \
                                  'Kuppel des Hauptgebäudes befindet sich eine goldene Statue der Jungfrau Maria. ' \
                                  'Unmittelbar vor dem Hauptgebäude und gegenüber befindet sich eine kupferne ' \
                                  'Christusstatue mit Waffen, die mit der Legende "Venite Ad Me Omnes" emporgehoben ' \
                                  'sind.'
        self.orig_answer = [{
            "answer_start": 188,
            "text": "a copper statue of Christ"
        }]
        self.translated_answer = [{
            "answer_start": 224,
            "text": "eine Kupferstatue von Christus"
        }]
        self.squad_translation = SquadTranslation()

    def test_find_sentence_number(self):
        answer_start = 70
        result = self.squad_translation.find_sentence_number_in_context(answer_start, self.translated_context)
        self.assertEqual(result, 1)

    def test_find_sentence_number_bad_case(self):
        answer_start = 400
        result = self.squad_translation.find_sentence_number_in_context(answer_start, self.translated_context)
        self.assertEqual(result, None)

    def test_iterate_qas(self):
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
        result = self.squad_translation.iterate_qas(orig_context=self.orig_context, paragraph=paragraph,
                                                    translated_context=self.translated_context)

        self.assertEquals(result, paragraph['qas'])

    def test_iterate_answers(self):
        mocked_squad_translation = SquadTranslation(mock=False)
        mocked_squad_translation.translate_text = MagicMock(return_value='sich eine kupferne Christusstatue')
        mocked_squad_translation.find_sentence_number_in_context = MagicMock(return_value=3)
        mocked_squad_translation.find_answer_start_in_translated_context = MagicMock(return_value=224)

        result = mocked_squad_translation.iterate_answers(answers=self.translated_answer,
                                                          orig_context=self.orig_context,
                                                          translated_context=self.translated_context)

        self.assertEquals(result, [{'answer_start': 224, 'text': 'sich eine kupferne Christusstatue'}])

    def test_iterate_answers_bad_case(self):
        mocked_squad_translation = SquadTranslation(mock=False)
        mocked_squad_translation.translate_text = MagicMock(return_value='bla bla bla')
        mocked_squad_translation.find_sentence_number_in_context = MagicMock(return_value=3)
        mocked_squad_translation.find_answer_start_in_translated_context = MagicMock(return_value=-1)

        answers = [{"answer_start": 123, "text": "not findable text in translated context bla bla bla"}]
        result = mocked_squad_translation.iterate_answers(answers=answers,
                                                          orig_context=self.orig_context,
                                                          translated_context=self.translated_context)

        self.assertEquals(result, [])

    def test_search_existing_chkp_file(self):
        input_file_path = 'data/train-v1.1_one_paragraph.json'
        output_file_path = 'data/train-v1.1_translated.json_chkp1'

        with open(input_file_path, 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())

        squad_dataset = json_data['data']
        result = self.squad_translation.search_existing_chkp_file(squad_dataset, output_file_path)
        assert result == 'data/train-v1.1_translated.json_chkp0'

    def test_search_existing_chkp_file_bad_case(self):
        input_file_path = 'data/train-v1.1_one_paragraph.json'
        output_file_path = 'data/train-v1.1.json'

        with open(input_file_path, 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())

        squad_dataset = json_data['data']
        result = self.squad_translation.search_existing_chkp_file(squad_dataset, output_file_path)
        assert result is None

    def test_chkp_file_length(self):
        input_file_path = 'data/train-v1.1_translated.json_chkp1'
        with open(input_file_path, 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())

        result = len(json_data['data'])
        assert result == 2

    def test_proceed_existing_chkp_file(self):
        input_file_path = 'data/train-v1.1_mock.json'
        output_file_path = 'data/train-v1.1_translated.json_chkp0'

        with open(input_file_path, 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())

        squad_dataset = json_data['data']
        result = self.squad_translation.strip_data_section_to_chkp_length(squad_dataset, output_file_path)

        assert len(result) == 2

    def test_search_answer_in_translated_context(self):  # TODO
        sentence_number = self.squad_translation.find_sentence_number_in_context(
            answer_start=self.orig_answer[0]['answer_start'],
            context=self.orig_context)
        answer_pos, p_result, sentence_number, substring = self.squad_translation \
            .find_sentence_with_answer_in_translated_context(sentence_number=sentence_number,
                                                             translated_answer_text=self.translated_answer[0]['text'],
                                                             translated_context=self.translated_context)

        self.assertEqual(answer_pos, 56)
        self.assertEqual(sentence_number, 2)
        self.assertEqual(substring, 'sich eine kupferne Christusstatue')

    def test_return_answer_start_good_case(self):
        sentence_number = self.squad_translation.find_sentence_number_in_context(
            answer_start=self.orig_answer[0]['answer_start'],
            context=self.orig_context)
        answer_start, translated_answer_text = self.squad_translation.find_answer_start_in_translated_context(
            sentence_number=sentence_number,
            translated_answer_text=self.translated_answer[0]['text'],
            translated_context=self.translated_context)

        self.assertEqual(answer_start, 214)
        self.assertEqual(translated_answer_text, 'sich eine kupferne Christusstatue')

    def test_return_answer_start_bad_case(self):
        sentence_number = self.squad_translation.find_sentence_number_in_context(self.orig_answer[0]['answer_start'],
                                                                                 self.orig_context)

        answer_start, translated_answer_text = self.squad_translation.find_answer_start_in_translated_context(
            sentence_number=sentence_number,
            translated_answer_text='bla bla bla',
            translated_context=self.translated_context)

        self.assertEqual(answer_start, -1)
        self.assertEqual(translated_answer_text, 'bla bla bla')

    def test_mock_translate_text(self):
        some_text = "dog"

        response = SquadTranslation(mock=True).translate_text(some_text)
        self.assertEqual(response, "dog")

    @skip("causes costs - run this test exclusively for checking Google Cloud Translation API access")
    def test_translate_text(self):
        some_text = "dog"

        response = SquadTranslation(mock=False).translate_text(some_text)
        self.assertEqual(response, "Hund")
