from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
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
    UniqueConstraint,
    Time,
    Uuid
)
from uuid import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, validates, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import event

from CodeGuard.models.enums import CourseStatus, CompletionStatus, Severity

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(Uuid(as_uuid=True, native_uuid=True), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    confirmed_on: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    enrollments: Mapped[List["Enrollments"]] = relationship(
        back_populates="user", cascade="all"
    )

    def __repr__(self):
        return f'User: id={self.id} username={self.username} password={self.password} email={self.email}'

class Courses(db.Model):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[CourseStatus] = mapped_column(Enum(CourseStatus),nullable=True, default=CourseStatus.DRAFT)

    module: Mapped[List["Modules"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    enrollments: Mapped[List["Enrollments"]] = relationship(
        back_populates="course", cascade="all"
    )
    exams: Mapped[List["Exams"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    image: Mapped["CourseImages"] = relationship(
        back_populates="course", cascade='all, delete-orphan'
    )
    def __repr__(self):
        return f'Course: name:{self.course_name} duration={self.duration} description={self.description} status={self.status}'

# Enrollment table
class Enrollments(db.Model):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    enrollment_date: Mapped[datetime.date] = mapped_column(Date)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    last_accessed_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    status: Mapped[CompletionStatus] = mapped_column(Enum(CompletionStatus), nullable=False, default=CompletionStatus.NOT_STARTED)
    exam_id: Mapped[Optional[int]] = mapped_column(ForeignKey("exams.id"), nullable=True, default=None)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["Users"] = relationship(back_populates="enrollments")
    course: Mapped["Courses"] = relationship(back_populates="enrollments")
    enrollments_modules: Mapped[List["EnrollmentsModules"]] = relationship(
        back_populates="enrollment", cascade="all, delete-orphan"
    )
    exam: Mapped["Exams"] = relationship(
        back_populates="enrollments"
    )
    exams_results: Mapped[List['ExamsResults']] = relationship(
        back_populates="enrollment", cascade='all, delete-orphan'
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'course_id', name='uq_enrolled_twice'),
    )

    def __repr__(self):
        return f'Enrollment: user:{self.user_id} course={self.course_id} date={self.enrollment_date} progress={self.progress}'


class Modules(db.Model):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    module_name: Mapped[str] = mapped_column(String(255), nullable=False)

    contents: Mapped[List["Contents"]] = relationship(
        back_populates="module", cascade='all, delete-orphan'
    )
    course: Mapped["Courses"] = relationship(back_populates="module")
    enrollments_modules: Mapped[List["EnrollmentsModules"]] = relationship(
        back_populates="module", cascade="all"
    )

    __table_args__ = (
        UniqueConstraint('course_id', 'order', name='uq_duplicate_modules'),
    )

    def __repr__(self):
        return f'Modules: course_id:{self.course_id} order={self.order} module_name={self.module_name}'

class EnrollmentsModules(db.Model):
    __tablename__ = "enrollments_modules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"), nullable=False)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), nullable=False)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[CompletionStatus] = mapped_column(Enum(CompletionStatus), nullable=False, default=CompletionStatus.NOT_STARTED)

    module: Mapped["Modules"] = relationship(
        back_populates='enrollments_modules'
    )
    enrollment: Mapped["Enrollments"] = relationship(
        back_populates='enrollments_modules'
    )
    users_contents: Mapped[List["UsersContents"]] = relationship(
        back_populates='enrollment_module', cascade='all'
    )

    __table_args__ = (
        UniqueConstraint('enrollment_id', 'module_id', name='uq_duplicate_progress'),
    )

    def __repr__(self):
        return f'id: {self.id} enrollment_id: {self.enrollment_id} module_id: {self.module_id} progress: {self.progress}'

class Contents(db.Model):
    __tablename__ = "contents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(60), nullable=False)
    
    module: Mapped["Modules"] = relationship(back_populates="contents")
    image: Mapped["ContentImages"] = relationship(
        back_populates='content', cascade='all, delete-orphan'
    )

    users_contents: Mapped[List["UsersContents"]] = relationship(
        back_populates='content', cascade='all'
    )

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
    question: Mapped["ChallengeQuestions"] = relationship(
        back_populates="content", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "challenges",
    }

class UsersContents(db.Model):
    __tablename__ = "users_contents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enrollment_module_id: Mapped[int] = mapped_column(ForeignKey('enrollments_modules.id'), nullable=False)
    content_id: Mapped[int] = mapped_column(ForeignKey('contents.id'), nullable=False)
    status: Mapped[CompletionStatus] = mapped_column(Enum(CompletionStatus), nullable=False, default=CompletionStatus.NOT_STARTED)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    option_selected: Mapped[Optional[int]] = mapped_column(ForeignKey("options.id"), nullable=True, default=None)
    answer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    correct: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    enrollment_module: Mapped["EnrollmentsModules"] = relationship(
        back_populates='users_contents'
    )
    content: Mapped["Contents"] = relationship(
        back_populates='users_contents'
    )
    option: Mapped["ChallengeOptions"] = relationship(
        back_populates='users_contents'
    )

    __table_args__ = (
        UniqueConstraint('enrollment_module_id', 'content_id', name='uq_content_users'),
    )

class Exams(db.Model):
    __tablename__ = "exams"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    _duration: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    todo: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    questions: Mapped[List["ExamQuestions"]] = relationship(
        back_populates='content', cascade='all, delete-orphan'
    )
    course: Mapped["Courses"] = relationship(
        back_populates="exams"
    )
    enrollments: Mapped[List["Enrollments"]] = relationship(
        back_populates="exam"
    )
    exams_results: Mapped[List["ExamsResults"]] = relationship(
        back_populates="exam", cascade="save-update, merge, refresh-expire, expunge"
    )
    
    @hybrid_property
    def duration(self) -> timedelta:
        return timedelta(seconds=self._duration)
    
    @duration.inplace.setter
    def _duration_setter(self, value: timedelta | int) -> None:
        if isinstance(value, timedelta):
            self._duration = value.total_seconds()
        else:
            self._duration = value

    @duration.inplace.expression
    @classmethod
    def _duration_expression(cls):
        return cls._duration

    def __repr__(self):
        return f'Exams: duration:{self.duration}'
    
class ExamsResults(db.Model):
    __tablename__ = "exams_results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey('enrollments.id'), nullable=False)
    exam_id: Mapped[Optional[int]] = mapped_column(ForeignKey('exams.id'), nullable=True, default=None)
    check_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    lines: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), nullable=True, default=None)

    enrollment: Mapped["Enrollments"] = relationship(
        back_populates="exams_results"
    )
    exam: Mapped["Exams"] = relationship(
        back_populates="exams_results"
    )


    def __repr__(self):
        return f'exam_id: {self.exam_id}, enrollment_id: {self.enrollment_id}, check_id: {self.check_id}'


class Questions(db.Model):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(80), nullable=False, default='standard')
    question_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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
    content_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contents.id"), nullable=True)
    content: Mapped["ContentsChallenges"] = relationship(
        back_populates='question'
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
    users_contents: Mapped[List["UsersContents"]] = relationship(
        back_populates='option', cascade="save-update, merge, refresh-expire, expunge"
    )


class Images(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(80), nullable=False, default='standard')
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    new_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "standard",
        "polymorphic_on": type,
    }
    def __repr__(self):
        return f'Images: ori:{self.original_filename} new_filename={self.new_filename} location={self.location}'

class ContentImages(Images):
    __mapper_args__ = {
        "polymorphic_identity": "content",
    }
    content_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contents.id"), unique=True, nullable=True, default=None)
    content: Mapped["Contents"] = relationship(
        back_populates="image", single_parent=True
    )

class CourseImages(Images):
    __mapper_args__ = {
        "polymorphic_identity": "course",
    }
    course_id: Mapped[Optional[int]] = mapped_column(ForeignKey("courses.id"), unique=True, nullable=True, default=None)
    course: Mapped["Courses"] = relationship(
        back_populates="image", single_parent=True
    )

@event.listens_for(Images, 'before_delete', propagate=True)
def before_delete_image(mapper, connection, target):
    from CodeGuard.utils.files import delete_from_storage
    delete_from_storage(filename=target.location)