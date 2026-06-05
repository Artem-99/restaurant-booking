from ninja import Schema


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
