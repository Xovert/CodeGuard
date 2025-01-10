from flask import current_app as app
import enum
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Boolean, 
    Integer, 
    String, 
    ForeignKey, 
    Date, 
    LargeBinary, 
    DateTime, 
    Text,
    Enum,
    Float,
    UniqueConstraint
)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, validates, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    confirmed_on: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    enrollment: Mapped[List["Enrollments"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'User: id={self.id} username={self.username} password={self.password} email={self.email}'

class CourseStatus(enum.Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"

class Courses(db.Model):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[CourseStatus] = mapped_column(Enum(CourseStatus),nullable=True, default=CourseStatus.DRAFT)

    module: Mapped[List["Modules"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    enrollment: Mapped[List["Enrollments"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    exams: Mapped[List["Exams"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f'Course: name:{self.course_name} duration={self.duration} description={self.description} status={self.status}'

# Enrollment table
class Enrollments(db.Model):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete='CASCADE'))
    enrollment_date: Mapped[datetime.date] = mapped_column(Date)
    progress: Mapped[int] = mapped_column(Integer, nullable=False)
    last_enrolled_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="enrollment")
    course: Mapped["Courses"] = relationship(back_populates="enrollment")

    def __repr__(self):
        return f'Enrollment: user:{self.user_id} course={self.course_id} date={self.enrollment_date} progress={self.progress}'


class Modules(db.Model):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete='CASCADE'), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    module_name: Mapped[str] = mapped_column(String(255), nullable=False)

    contents: Mapped[List["Contents"]] = relationship(
        back_populates="module", cascade='all, delete-orphan'
    )
    course: Mapped["Courses"] = relationship(back_populates="module")

    __table_args__ = (
        UniqueConstraint('course_id', 'order', name='uq_duplicate_modules'),
    )

    def __repr__(self):
        return f'Modules: course_id:{self.course_id} order={self.order} module_name={self.module_name}'


class Images(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    content_id: Mapped[int] = mapped_column(ForeignKey("contents.id"), unique=True, nullable=False)
    
    content: Mapped["Contents"] = relationship(
        back_populates="image", single_parent=True
    )
    def __repr__(self):
        return f'Images: ori:{self.original_filename} new_filename={self.new_filename} location={self.location} content_id={self.content_id}'


class Contents(db.Model):
    __tablename__ = "contents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete='CASCADE'), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(60), nullable=False)
    
    module: Mapped["Modules"] = relationship(back_populates="contents")
    image: Mapped["Images"] = relationship(back_populates='content', cascade='all, delete-orphan')

    __mapper_args__ = {
        "polymorphic_identity": "standard",
        "polymorphic_on": type,
    }
    __table_args__ = (
        UniqueConstraint('module_id', 'order', name='uq_duplicate_contents'),
    )


    def __repr__(self):
        return f'Contents: module_id:{self.module_id} order={self.order} type={self.type}'


class ContentsLearning(Contents):
    content_body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "learning",
    }

class ContentsChallenges(Contents):
    questions: Mapped[List["ChallengeQuestions"]] = relationship(
        back_populates="content", cascade="all, delete-orphan"
    )
    __mapper_args__ = {
        "polymorphic_identity": "challenges",
    }

class Exams(db.Model):
    __tablename__ = "exams"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    questions: Mapped[List["ExamQuestions"]] = relationship(
        back_populates='content', cascade='all, delete-orphan'
    )
    course: Mapped["Courses"] = relationship(
        back_populates="exams"
    )

    def __repr__(self):
        return f'Exams: duration:{self.duration}'


class Questions(db.Model):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(80), nullable=False, default='standard')
    question_text: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "standard",
        "polymorphic_on": type,
    }

    def __repr__(self):
        return f'Questions: type:{self.type} question_text={self.question_text}'


class ExamQuestions(Questions):
    __mapper_args__ = {
        "polymorphic_identity": "exam",
    }
    exam_id: Mapped[Optional[int]] = mapped_column(ForeignKey("exams.id"), nullable=True)
    content: Mapped["Exams"] = relationship(
        back_populates='questions'
    )
    options: Mapped[List["ExamOptions"]] = relationship(
        back_populates="question", cascade='all, delete-orphan'
    )


class ChallengeQuestions(Questions):
    __mapper_args__ = {
        "polymorphic_identity": "challenge",
    }
    content_id: Mapped[int] = mapped_column(ForeignKey("contents.id"))
    content: Mapped["ContentsChallenges"] = relationship(
        back_populates='questions'
    )
    options: Mapped[List["ChallengeOptions"]] = relationship(
        back_populates="question", cascade='all, delete-orphan'
    )


class Options(db.Model):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(80), nullable=False, default='standard')
    option_text: Mapped[str] = mapped_column(String(255), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    __mapper_args__ = {
        "polymorphic_identity": "standard",
        "polymorphic_on": type,
    }
    def __repr__(self):
        return f'Options: type:{self.type} option_text={self.option_text} is_correct={self.is_correct} question_id={self.question_id}'


class ExamOptions(Options):
    __mapper_args__ = {
        "polymorphic_identity": "exam",
    }

    question: Mapped["ExamQuestions"] = relationship(
        back_populates='options'
    )


class ChallengeOptions(Options):
    __mapper_args__ = {
        "polymorphic_identity": "challenge",
    }

    question: Mapped["ChallengeQuestions"] = relationship(
        back_populates='options'
    )