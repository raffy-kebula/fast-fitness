from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, List
import datetime
import re


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

    @field_validator("name", "surname")
    def name_letters_only(cls, v):
        if not v.isalpha():
            raise ValueError("Name and surname must contain only letters")
        if len(v) < 2:
            raise ValueError("Name and surname must be at least 2 characters")
        return v

    @field_validator("date_of_birth")
    def check_birth_date(self, v):
        if v > datetime.date.today():
            raise ValueError("Date of birth must not be in the future")
        return v

    @field_validator("username")
    def username_length(self, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return v

    @field_validator("password")
    def password_strength(self, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("location_of_birth", "city")
    def location_length(self, v):
        if not v or len(v) < 2:
            raise ValueError("Location and city must be at least 2 characters")
        return v

    @field_validator("country")
    def country_length(self, v):
        if not v or len(v) < 2:
            raise ValueError("Country must be at least 2 characters")
        return v

    @field_validator("street_address")
    def street_address_length(self, v):
        if not v or len(v) < 2:
            raise ValueError("Street address must be at least 2 characters")
        return v

    @field_validator("street_number")
    def street_number_positive(self, v):
        if v <= 0:
            raise ValueError("Street number must be positive")
        return v

    @field_validator("zip_code")
    def zip_code_format(self, v):
        if not v.isdigit() or len(v) < 4 or len(v) > 10:
            raise ValueError("ZIP code must be numeric and between 4 and 10 digits")
        return v

    @field_validator("phone_number")
    def phone_number_format(self, v):
        if not re.fullmatch(r"^\+\d{1,3}\s\d{6,14}$", v):
            raise ValueError("Phone number must be in international format, e.g., +39 123456789")
        return v


# no password on response
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


class CreditCardCreateORM(BaseModel):
    id: int
    user_id: int
    token: str          # generic token by Payment Service Provider
    last_4: str
    brand: str

    model_config = {"from_attributes": True}

    @field_validator("token")
    def token_length(self, v):
        if not v or len(v) < 128:
            raise ValueError("Token must be at least 128 characters")
        return v

    @field_validator("last_4")
    def last4_length(self, v):
        if not v or len(v) < 4:
            raise ValueError("Necessary last four digits of credit card")
        return v

    @field_validator("brand")
    def brand_length(self, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Brand must be between 3 and 50 characters")
        return v


# no token on response
class CreditCardOutORM(BaseModel):
    id: int
    user_id: int
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

    @field_validator("duration_month", "weekly_accesses")
    def positive_numbers(self, v):
        if v <= 0:
            raise ValueError("Value must be positive")
        return v

    @field_validator("cost")
    def cost_positive(self, v):
        if v < 0:
            raise ValueError("Cost must be non-negative")
        return v


class SubscriptionUserCardORM(BaseModel):
    id: int
    user_id: int
    card_id: int
    subscription_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    automatic_renewal: bool = False

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    def check_dates(self, values):
        init = values.get("init_date")
        expiry = values.get("expiry_date")
        if init and expiry and expiry <= init:
            raise ValueError("expiry_date must be after init date")
        return values


class CourseORM(BaseModel):
    id: int
    type: str
    description: Optional[str] = None
    n_accesses: int
    cost: float
    duration_month: int
    require_subscription: bool = False

    model_config = {"from_attributes": True}

    @field_validator("type")
    def type_length(self, v):
        if not v or len(v) < 2:
            raise ValueError("Course type must have at least 2 characters")
        return v

    @field_validator("n_accesses", "duration_month")
    def positive_numbers(self, v):
        if v <= 0:
            raise ValueError("Value must be positive")
        return v

    @field_validator("cost")
    def cost_positive(self, v):
        if v < 0:
            raise ValueError("Cost must be non-negative")
        return v


class CourseUserCardORM(BaseModel):
    id: int
    user_id: int
    card_id: int
    course_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    automatic_renewal: bool = False

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    def check_dates(self, values):
        init = values.get("init_date")
        expiry = values.get("expiry_date")
        if init and expiry and expiry <= init:
            raise ValueError("expiry_date must be after init date")
        return values


class ReservationCourseORM(BaseModel):
    id: int
    user_id: int
    course_id: int
    date: datetime.date
    from_hour: datetime.time
    to_hour: datetime.time

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    def check_hours(self, values):
        from_hour = values.get("from_hour")
        to_hour = values.get("to_hour")

        if from_hour < datetime.datetime.now().hour:
            raise ValueError("from_hour must be selected")

        if from_hour and to_hour and to_hour <= from_hour:
            raise ValueError("to_hour must be after from_hour")
        return values

    @field_validator("date")
    def check_date(self, v):
        if v < datetime.date.today():
            raise ValueError("Date must not be in the past")
        return v


class WeekDay(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

class ExerciseORM(BaseModel):
    id: int
    name: str
    muscle_group: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}

    @field_validator("name")
    def name_length(cls, v):
        if len(v) < 3 or len(v) > 100:
            raise ValueError("Name must be between 3 and 100 characters")
        return v

    @field_validator("muscle_group")
    def muscle_group_length(cls, v):
        if len(v) < 3 or len(v) > 100:
            raise ValueError("Muscle Group must be between 3 and 100 characters")
        return v


class TrainingCardExerciseORM(BaseModel):
    id: int
    exercise_id: int
    position: int
    day_execution: WeekDay
    sets: int
    reps: int
    weight: Optional[float] = None

    model_config = {"from_attributes": True}

    @field_validator("position")
    def position_valid(self, v):
        if v < 1 or v > 12:
            raise ValueError("Position must be between 1 and 12")
        return v

    @field_validator("sets")
    def sets_valid(self, v):
        if v < 1 or v > 50:
            raise ValueError("Sets must be between 1 and 50")
        return v

    @field_validator("reps")
    def reps_valid(self, v):
        if v < 1 or v > 20:
            raise ValueError("Reps must be between 1 and 20")
        return v

    @field_validator("position")
    def position_valid(self, v):
        if v < 1 or v > 12:
            raise ValueError("Position must be between 1 and 12")
        return v

    @field_validator("day_execution")
    def day_execution_valid(self, v):
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        if v not in valid_days:
            raise ValueError(f"Day Execution must be one of {valid_days}")
        return v


class TrainingCardORM(BaseModel):
    id: int
    user_id: int
    init_date: datetime.date
    expiry_date: datetime.date
    description: Optional[str] = None
    note: Optional[str] = None
    exercises: List[TrainingCardExerciseORM] = []

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    def check_dates(self, values):
        init = values.get("init_date")
        expiry = values.get("expiry_date")
        if init and expiry and expiry <= init:
            raise ValueError("expiry_date must be after init date")
        return values