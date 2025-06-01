import csv

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Answer, Difficult_Level, Question
from app.schemas import DifficultLevelCreate, QuestionCreate
from app.settings import settings


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
            Answer(
                text=answer.text,
                is_correct=answer.is_correct
            ) for answer in dto.answers
        ]
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        return new_question
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Ошибка при сохранении вопроса: {str(e)}")


def main():

    DIFF_LEVELS = ('Легкий', 'Средний', 'Сложный', 'Финал')
    QUESTION_FILE = 'test-data/questions.csv'

    engine = create_engine(settings.get_database_url())
    session = Session(engine)

    # Создаемм уровни сложности.
    for level in DIFF_LEVELS:
        create_diff_level(DifficultLevelCreate(name=level), session)
    # Создаем вопросы из csv.
    with open(QUESTION_FILE) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for (
            diff_level,
            question,
            answer_a,
            answer_b,
            answer_c,
            answer_d,
            correct_answer
        ) in reader:
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


if __name__ == '__main__':
    main()
