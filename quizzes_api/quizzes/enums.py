from enum import Enum


class QuestionsTypeEnum(Enum):
    TEXT = 'текстовый ответ'
    SINGLE = 'ответ с одним вариантом'
    MULTIPLE = 'ответ с выбором нескольких вариантов'

    @staticmethod
    def get_choices():
        return [(tag.name, tag.value) for tag in QuestionsTypeEnum]
