from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db.funcs import get_db
from app.db.models import Question

app = FastAPI()


@app.get("/api/v1/questions/")
def get_question(db: Session = Depends(get_db)):
    """Возвращает все вопросы."""
    return db.query(Question).all()


@app.get("/api/v1/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Возвращает вопрос."""
    return db.query(Question).get(question_id)
