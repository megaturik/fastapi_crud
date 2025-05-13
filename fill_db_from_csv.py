import csv

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import Answer, Difficult_Level, Question
from app.db.schemas import DifficultLevelCreate, QuestionCreate
from app.settings import settings

diff_levels = ('Легкий', 'Средний', 'Сложный', 'Финал')

engine = create_engine(settings.get_database_url(), echo=True)
session = Session(engine)


def create_diff_level(dto: DifficultLevelCreate, db: Session):
    level = Difficult_Level(**dto.model_dump())
    db.add(level)
    db.commit()
    db.refresh(level)
    return level


def create_question(dto: QuestionCreate, db: Session):
    try:
        new_question = Question(text=dto.text, difficult_id=dto.difficult_id)
        new_question.answers = [
            Answer(text=answer.text, is_correct=answer.is_correct) for answer in dto.answers
        ]
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        return new_question
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Ошибка при сохранении вопроса: {str(e)}")


for level in diff_levels:
    create_diff_level(DifficultLevelCreate(name=level), session)


with open('questions.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for diff_level, question, answer_a, answer_b, answer_c, answer_d, correct_answer in reader:
        correct_answer = int(correct_answer)
        data = {
            "text": question,
            "difficult_id": diff_level,
            "answers": [
                {"text": answer_a, "is_correct": 1 == correct_answer},
                {"text": answer_b, "is_correct": 2 == correct_answer},
                {"text": answer_c, "is_correct": 3 == correct_answer},
                {"text": answer_d, "is_correct": 4 == correct_answer}
            ]
        }
        question = create_question(QuestionCreate(**data), db=session)
