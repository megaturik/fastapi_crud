from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Answer, Question
from app.schemas import QuestionCreate, QuestionList, QuestionRead

app = FastAPI()


@app.get("/api/v1/questions/", response_model=List[QuestionList])
def get_question(db: Session = Depends(get_db)):
    """Возвращает все вопросы."""
    return db.query(Question).all()


@app.post("/api/v1/questions/")
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """Создает новый вопрос."""
    new_question = Question(
        text=question.text,
        difficult_id=question.difficult_id
    )
    new_question.answers = [
        Answer(
            text=answer.text,
            is_correct=answer.is_correct
        ) for answer in question.answers
    ]
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@app.get("/api/v1/questions/{question_id}", response_model=QuestionRead)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Возвращает вопрос."""
    question = db.query(Question).get(question_id)
    if question is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="question not found")
    return question
