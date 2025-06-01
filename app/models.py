from datetime import datetime, timezone
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)

Base = declarative_base()


class Difficult_Level(Base):
    """Представляет уровень сложности вопросов."""

    __tablename__ = "difficult_levels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    questions: Mapped[List["Question"]] = (
        relationship(back_populates="difficulty")
    )


class Question(Base):
    """Представляет вопрос викторины."""

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False, unique=False)
    difficult_id: Mapped[int] = mapped_column(ForeignKey(Difficult_Level.id))
    difficulty: Mapped["Difficult_Level"] = (
        relationship(back_populates="questions")
    )
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan")


class Answer(Base):
    """Представляет вариант ответа на вопрос."""

    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Question.id, ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    question: Mapped["Question"] = relationship(back_populates="answers")


class Player(Base):
    """Представляет игрока в викторине."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(
        String(320), nullable=False, unique=True)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False)
    total_games_played: Mapped[int] = mapped_column(Integer, default=0)
