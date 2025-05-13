from http import HTTPStatus
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db.funcs import get_db
from app.db.models import Question
from app.db.schemas import QuestionRead

app = FastAPI()


@app.get("/api/v1/questions/")
def get_question(db: Session = Depends(get_db)):
    """Возвращает все вопросы."""
    return db.query(Question).all()


@app.get("/api/v1/questions/{question_id}", response_model=QuestionRead)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Возвращает вопрос."""
    question = db.query(Question).get(question_id)
    if question is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="question not found")
    return question
