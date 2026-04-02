from sqlalchemy import (
    Column, Integer, String, Float, Numeric, Date, ForeignKey, Boolean, Time
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# USERS & PAYMENT
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    location_of_birth = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    street_address = Column(String(255), nullable=False)
    street_number = Column(Integer, nullable=False)
    city = Column(String(100), nullable=False)
    zip_code = Column(String(10), nullable=False)
    phone_number = Column(String(20), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # relationship
    credit_cards = relationship("CreditCard", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("SubscriptionUserCard", back_populates="user", cascade="all, delete-orphan")
    courses = relationship("CourseUserCard", back_populates="user", cascade="all, delete-orphan")
    reservations = relationship("ReservationCourse", back_populates="user", cascade="all, delete-orphan")
    training_cards = relationship("TrainingCard", back_populates="user", cascade="all, delete-orphan")


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(128))
    last_4 = Column(String(4))
    brand = Column(String(50))

    # relationship
    user = relationship("User", back_populates="credit_cards")
    subscriptions = relationship("SubscriptionUserCard", back_populates="card")
    courses = relationship("CourseUserCard", back_populates="card")


# SUBSCRIPTIONS & COURSES
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    cost = Column(Numeric(10, 2), nullable=False)
    duration_month = Column(Integer, nullable=False)
    weekly_accesses = Column(Integer, nullable=False)
    description = Column(String(255))

    # relationship
    users_cards = relationship("SubscriptionUserCard", back_populates="subscription", cascade="all, delete-orphan")


class SubscriptionUserCard(Base):
    __tablename__ = "subscription_user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    init_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    automatic_renewal = Column(Boolean, default=False)

    # relationship
    user = relationship("User", back_populates="subscriptions")
    card = relationship("CreditCard", back_populates="subscriptions")
    subscription = relationship("Subscription", back_populates="users_cards")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    description = Column(String(255))
    n_accesses = Column(Integer, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    duration_month = Column(Integer, nullable=False)
    require_subscription = Column(Boolean, default=False)

    # relationship
    users_cards = relationship("CourseUserCard", back_populates="course", cascade="all, delete-orphan")
    reservations = relationship("ReservationCourse", back_populates="course", cascade="all, delete-orphan")


class CourseUserCard(Base):
    __tablename__ = "course_user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    init_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    automatic_renewal = Column(Boolean, default=False)

    # relationship
    user = relationship("User", back_populates="courses")
    card = relationship("CreditCard", back_populates="courses")
    course = relationship("Course", back_populates="users_cards")


class ReservationCourse(Base):
    __tablename__ = "reservation_courses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    date = Column(Date, nullable=False)
    from_hour = Column(Time, nullable=False)
    to_hour = Column(Time, nullable=False)

    # relationship
    user = relationship("User", back_populates="reservations")
    course = relationship("Course", back_populates="reservations")


# TOPOLOGY OF EXERCISES
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    muscle_group = Column(String(100), nullable=False)
    description = Column(String(255))

    # relationship
    training_exercises = relationship("TrainingExercise", back_populates="exercise", cascade="all, delete-orphan")


# GENERIC TRAINING EXERCISE
class TrainingExercise(Base):
    __tablename__ = "training_exercises"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float)

    # relationship
    exercise = relationship("Exercise", back_populates="training_exercises")
    card_exercises = relationship("TrainingCardExercise", back_populates="training_exercise", cascade="all, delete-orphan")


# TRAINING CARDS
class TrainingCard(Base):
    __tablename__ = "training_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    init_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    description = Column(String(255))
    note = Column(String(255))

    # relationship
    user = relationship("User", back_populates="training_cards")
    exercises = relationship("TrainingCardExercise", back_populates="training_card", cascade="all, delete-orphan")


# TRAINING CARD EXERCISE (position + day per user)
class TrainingCardExercise(Base):
    __tablename__ = "training_card_exercises"

    id = Column(Integer, primary_key=True, index=True)
    training_card_id = Column(Integer, ForeignKey("training_cards.id"), nullable=False)
    training_exercise_id = Column(Integer, ForeignKey("training_exercises.id"), nullable=False)
    position = Column(Integer, nullable=False)
    day_execution = Column(String(20), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float)

    # relationship
    training_card = relationship("TrainingCard", back_populates="exercises")
    training_exercise = relationship("TrainingExercise", back_populates="card_exercises")