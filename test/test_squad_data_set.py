import json
from unittest import TestCase

from squad_data_set import SquadSetSchema, Answers, Qas, Paragraphs, Data, SquadDataSet


class TestSquadDataSet(TestCase):

    def test_deserialization(self):  # JSON to Object
        with open("data\\train-v1.1_mock.json", 'r', encoding='utf-8') as f:
            incoming_json = json.loads(f.read())

        squad_set_schema = SquadSetSchema()
        squad_set = squad_set_schema.load(incoming_json)

        first_title = squad_set.data[0].title
        first_paragraph = squad_set.data[0].paragraphs[0]
        first_answer_text = first_paragraph.qas[0].answers[0].text
        first_id = first_paragraph.qas[0].id
        second_qas_answer_start = first_paragraph.qas[1].answers[0].answer_start

        assert first_answer_text == 'Saint Bernadette Soubirous'
        assert first_title == 'University_of_Notre_Dame'
        assert first_id == "5733be284776f41900661182"
        assert second_qas_answer_start == 188

    def test_serialization(self):  # Object to JSON
        with open("data\\train-v1.1_mock_short.json", 'r', encoding='utf-8') as f:
            expected_json = json.loads(f.read())

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
        squad_set = SquadDataSet(data=[data], version=version)

        squad_set_schema = SquadSetSchema()
        result = squad_set_schema.dump(squad_set)

        assert result == expected_json

    def test_deserialization_dev_set(self):  # JSON to Object
        with open("data\\dev-v1.1_mock.json", 'r', encoding='utf-8') as f:
            incoming_json = json.loads(f.read())

        squad_set_schema = SquadSetSchema()
        squad_set = squad_set_schema.load(incoming_json)

        first_title = squad_set.data[0].title
        first_paragraph = squad_set.data[0].paragraphs[0]
        first_answer_text = first_paragraph.qas[0].answers[0].text
        first_id = first_paragraph.qas[0].id
        second_qas_answer_start = first_paragraph.qas[1].answers[0].answer_start

        assert first_answer_text == 'Denver Broncos'
        assert first_title == 'Super_Bowl_50'
        assert first_id == "56be4db0acb8001400a502ec"
        assert second_qas_answer_start == 249

    def test_serialization_dev_set(self):  # Object to JSON
        with open("data\\dev-v1.1_mock_short.json", 'r', encoding='utf-8') as f:
            expected_json = json.loads(f.read())

        title = "Super_Bowl_50"
        context = "Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24–10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the \"golden anniversary\" with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as \"Super Bowl L\"), so that the logo could prominently feature the Arabic numerals 50."

        version = "1.1"

        question1 = "Which NFL team represented the AFC at Super Bowl 50?"
        id1 = "56be4db0acb8001400a502ec"
        answer1 = Answers(answer_start=177, text="Denver Broncos")
        answer2 = Answers(answer_start=177, text="Denver Broncos")
        answer3 = Answers(answer_start=177, text="Denver Broncos")

        question2 = "What 2015 NFL team one the AFC playoff?"
        id2 = "56d9895ddc89441400fdb510"
        answer5 = Answers(answer_start=177, text="Denver Broncos")
        answer6 = Answers(answer_start=177, text="Denver Broncos")
        answer7 = Answers(answer_start=177, text="Denver Broncos")

        qas1 = Qas(answers=[answer1, answer2, answer3], question=question1, id=id1)
        qas2 = Qas(answers=[answer5, answer6, answer7], question=question2, id=id2)
        paragraphs = Paragraphs(context=context, qas=[qas1, qas2])
        data = Data(title=title, paragraphs=[paragraphs])
        squad_set = SquadDataSet(data=[data], version=version)

        train_set_schema = SquadSetSchema()
        result = train_set_schema.dump(squad_set)

        assert result == expected_json
