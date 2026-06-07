from ninja import Schema
from typing import Optional
from datetime import date, time, datetime


# Пользователи
class RegisterIn(Schema):
    email: str
    password: str
    first_name: str


class LoginIn(Schema):
    email: str
    password: str


class UserOut(Schema):
    id: int
    email: str
    first_name: str
    is_staff: bool


class TokenOut(Schema):
    access_token: str
    token_type: str = "bearer"


# Столики
class TableOut(Schema):
    id: int
    number: int
    name: str
    capacity: int
    location: str
    description: str
    is_available: bool
    is_booked_today: bool = False


class TableIn(Schema):
    number: int
    name: str
    capacity: int
    location: str = "Основной зал"
    description: str = ""
    is_available: bool = True


class TableUpdate(Schema):
    name: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None


# Бронирования
class BookingIn(Schema):
    table_id: int
    date: date
    start_time: time
    guests_count: int = 1
    comment: str = ""


class TableInfo(Schema):
    id: int
    number: int
    name: str
    location: str

    class Config:
        from_attributes = True


class UserInfo(Schema):
    id: int
    email: str
    first_name: str

    class Config:
        from_attributes = True


class BookingOut(Schema):
    id: int
    table: TableInfo
    user: UserInfo
    date: date
    start_time: time
    guests_count: int
    comment: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
