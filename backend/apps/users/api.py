from ninja import Router
from ninja.errors import HttpError
from .models import User
from .schemas import RegisterIn, LoginIn, UserOut, TokenOut
from .auth import create_token, auth

router = Router(tags=["auth"])


@router.post("/register", response=UserOut)
def register(request, data: RegisterIn):
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email уже зарегистрирован")
    user = User(
        username=data.email,
        email=data.email,
        first_name=data.first_name,
        is_staff=False,
    )
    user.set_password(data.password)
    user.save()
    return user


@router.post("/login", response=TokenOut)
def login(request, data: LoginIn):
    try:
        user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        raise HttpError(401, "Неверный email или пароль")
    if not user.check_password(data.password):
        raise HttpError(401, "Неверный email или пароль")
    return {"access_token": create_token(user.id)}


@router.get("/me", auth=auth, response=UserOut)
def me(request):
    return request.auth


@router.get("/users", auth=auth, response=list[UserOut])
def list_users(request):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    return list(User.objects.all())


@router.post("/users/{user_id}/toggle-role", auth=auth, response=UserOut)
def toggle_role(request, user_id: int):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HttpError(404, "Пользователь не найден")
    if user.id == request.auth.id:
        raise HttpError(400, "Нельзя изменить собственную роль")
    user.is_staff = not user.is_staff
    user.save()
    return user
