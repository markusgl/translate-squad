import json
from unittest import TestCase

from train_set import TrainSetSchema, Answers, Qas, Paragraphs, Data, TrainSet


class TestTrainSet(TestCase):

    def test_deserialization(self):
        with open("data\\train-v1.1_mock.json", 'r', encoding='utf-8') as f:
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

    def test_serialization(self):
        with open("data\\train-v1.1_mock_short.json", 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())

        title = "University_of_Notre_Dame"
        context = "Architecturally, the school has a Catholic character. Atop the Main Building's gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend \"Venite Ad Me Omnes\". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary."
        answer_start = 515
        answer_text = "Saint Bernadette Soubirous"
        question = "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?"
        id = "5733be284776f41900661182"
        version = "1.1"

        answers = Answers(answer_start=answer_start, text=answer_text)
        qas = Qas(answers=[answers], question=question, id=id)
        paragraphs = Paragraphs(context=context, qas=[qas])
        data = Data(title=title, paragraphs=[paragraphs])
        train_set = TrainSet(data=[data], version=version)

        train_set_schema = TrainSetSchema()
        result = train_set_schema.dump(train_set)

        assert result == json_data
