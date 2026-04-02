import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import EmailStr


class User(BaseModel):
    id: int
    name: str
    surname: str
    date_of_birth: datetime.date
    location_of_birth: str
    country: str
    street_address: str
    street_number: int
    city: str
    zip_code: str
    phone_number: str
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class CreditCard(BaseModel):
    id: int
    user_id: int
    token: str  # generic token by Payment Service Provider
    last_4: str
    brand: str

    class Config:
        orm_mode = True


class Subscription(BaseModel):
    id: int
    cost: float
    duration_month: int
    weekly_accesses: int
    description: Optional[str] = None

    class Config:
        orm_mode = True


class SubscriptionUserCard(BaseModel):
    id: int
    user_id: int
    card_id: int
    subscription_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    automatic_renewal: bool = False

    class Config:
        orm_mode = True


class Course(BaseModel):
    id: int
    type: str
    description: str
    n_accesses: int
    cost: float
    duration_month: int
    require_subscription: bool = False

    class Config:
        orm_mode = True


class CourseUserCard(BaseModel):
    id: int
    user_id: int
    card_id: int
    course_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    automatic_renewal: bool = False

    class Config:
        orm_mode = True


class ReservationCourse(BaseModel):
    id: int
    user_id: int
    course_id: int
    date: datetime.date
    from_hour: datetime.time
    to_hour: datetime.time

    class Config:
        orm_mode = True


class Exercise(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    muscle_group: str

    class Config:
        orm_mode = True


class TrainingExercise(BaseModel):
    id: int
    exercise_id: int
    sets: int
    reps: int
    weight: Optional[float] = None
    order: int
    note: Optional[str] = None

    class Config:
        orm_mode = True


class TrainingCard(BaseModel):
    id: int
    user_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    description: Optional[str] = None
    note: Optional[str] = None
    exercise_ids: list[int]

    class Config:
        orm_mode = True






