from typing import List

from pydantic import BaseModel, Field, field_validator


class DifficultLevelCreate(BaseModel):
    name: str = Field(example="Легкий")


class AnswerCreate(BaseModel):
    text: str = Field(example="Париж")
    is_correct: bool = Field(example=True)


class QuestionCreate(BaseModel):
    text: str = Field(example="Столица Франции?")
    difficult_id: int = Field(example=1)
    answers: List[AnswerCreate]

    @field_validator('answers', mode='after')
    @classmethod
    def check_answers(cls, value: List):
        if len(value) != 4:
            raise ValueError("Нам нужно 4 ответа для каждого вопроса.")
        if sum(answer.is_correct for answer in value) != 1:
            raise ValueError("Один из ответов должен быть правильным.")
        if len(value) != len(set(answer.text for answer in value)):
            raise ValueError("Все ответы должны быть уникальными.")
        return value


class QuestionList(BaseModel):
    id: int = Field(example=1)
    text: str = Field(example="Столица Франции?")


class QuestionRead(BaseModel):
    text: str = Field(example="Столица Франции?")
    answers: List[AnswerCreate]
