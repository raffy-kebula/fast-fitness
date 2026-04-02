from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime


class UserCreateORM(BaseModel):
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
    password: str  # hash in backend

    model_config = {"from_attributes": True}


class UserOutORM(BaseModel):
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

    model_config = {"from_attributes": True}


class CreditCardORM(BaseModel):
    id: int
    user_id: int
    token: str          # generic token by Payment Service Provider
    last_4: str
    brand: str

    model_config = {"from_attributes": True}


class SubscriptionORM(BaseModel):
    id: int
    cost: float
    duration_month: int
    weekly_accesses: int
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class SubscriptionUserCardORM(BaseModel):
    id: int
    user_id: int
    card_id: int
    subscription_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    automatic_renewal: bool = False

    model_config = {"from_attributes": True}


class CourseORM(BaseModel):
    id: int
    type: str
    description: Optional[str] = None
    n_accesses: int
    cost: float
    duration_month: int
    require_subscription: bool = False

    model_config = {"from_attributes": True}


class CourseUserCardORM(BaseModel):
    id: int
    user_id: int
    card_id: int
    course_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    automatic_renewal: bool = False

    model_config = {"from_attributes": True}


class ReservationCourseORM(BaseModel):
    id: int
    user_id: int
    course_id: int
    date: datetime.date
    from_hour: datetime.time
    to_hour: datetime.time

    model_config = {"from_attributes": True}


class ExerciseORM(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    muscle_group: str

    model_config = {"from_attributes": True}


class TrainingExerciseORM(BaseModel):
    id: int
    exercise_id: int
    sets: int
    reps: int
    weight: Optional[float] = None
    position: int
    note: Optional[str] = None

    model_config = {"from_attributes": True}


class TrainingCardORM(BaseModel):
    id: int
    user_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    description: Optional[str] = None
    note: Optional[str] = None
    exercises: List[TrainingExerciseORM] = []

    model_config = {"from_attributes": True}



