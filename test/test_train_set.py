import json
from unittest import TestCase

from train_set import TrainSetSchema


class TestTrainSet(TestCase):

    def test_deserialization(self):
        with open("C:\\develop\\translate-squad\\test\\data\\train-v1.1_mock.json", 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())

        train_set_schema = TrainSetSchema()
        train_set = train_set_schema.load(json_data)

        first_title = train_set.data[0].title
        first_paragraph = train_set.data[0].paragraphs[0]
        first_answer_text = first_paragraph.qas[0].answers[0].text
        first_id = first_paragraph.qas[0].id
        second_answer_start = first_paragraph.qas[1].answers[0].answer_start

        assert first_answer_text == 'Saint Bernadette Soubirous'
        assert first_title == 'University_of_Notre_Dame'
        assert first_id == "5733be284776f41900661182"
        assert second_answer_start == 188

    def test_serialization(self): # TODO
        pass