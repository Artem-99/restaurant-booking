from ninja import Schema
from typing import Optional


class TableOut(Schema):
    id: int
    number: int
    name: str
    capacity: int
    location: str
    description: str
    is_available: bool


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
