from marshmallow import Schema, fields, post_load


class TrainSet:  # model
    def __init__(self, data: object, version: str):
        self.data = data
        self.version = version


class Data:
    def __init__(self, title: str, paragraphs: object):
        self.title = title
        self.paragraphs = paragraphs


class Paragraphs(object):
    def __init__(self, context: str, qas: object):
        self.context = context
        self.qas = qas


class Qas(object):
    def __init__(self, answers: object, question: str, id: str):
        self.answers = answers
        self.question = question
        self.id = id


class Answers(object):
    def __init__(self, answer_start: int, text: str):
        self.answer_start = answer_start
        self.text = text


class AnswersSchema(Schema):
    answer_start = fields.Int()
    text = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Answers(**data)


class QasSchema(Schema):
    answers = fields.List(fields.Nested(AnswersSchema))
    question = fields.Str()
    id = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Qas(**data)


class ParagraphsSchema(Schema):
    context = fields.Str()
    qas = fields.List(fields.Nested(QasSchema))

    @post_load
    def make_user(self, data, **kwargs):
        return Paragraphs(**data)


class DataSchema(Schema):
    title = fields.Str()
    paragraphs = fields.List(fields.Nested(ParagraphsSchema))

    @post_load
    def make_user(self, data, **kwargs):
        return Data(**data)


class TrainSetSchema(Schema):
    data = fields.List(fields.Nested(DataSchema))
    version = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return TrainSet(**data)
