from ninja import Schema
from datetime import date, time, datetime


class BookingIn(Schema):
    table_id: int
    date: date
    start_time: time
    end_time: time
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
    end_time: time
    guests_count: int
    comment: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
