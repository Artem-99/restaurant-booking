from ninja import Router
from ninja.errors import HttpError
from datetime import datetime
from .models import User, Table, Booking
from .schemas import (
    RegisterIn, LoginIn, UserOut, TokenOut,
    TableIn, TableUpdate, TableOut,
    BookingIn, BookingOut,
)
from .auth import create_token, auth


# ── Авторизация ──────────────────────────────────────────────────────────────

auth_router = Router(tags=["auth"])


@auth_router.post("/register", response=UserOut)
def register(request, data: RegisterIn):
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email уже зарегистрирован")
    user = User(username=data.email, email=data.email, first_name=data.first_name, is_staff=False)
    user.set_password(data.password)
    user.save()
    return user


@auth_router.post("/login", response=TokenOut)
def login(request, data: LoginIn):
    try:
        user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        raise HttpError(401, "Неверный email или пароль")
    if not user.check_password(data.password):
        raise HttpError(401, "Неверный email или пароль")
    return {"access_token": create_token(user.id)}


@auth_router.get("/me", auth=auth, response=UserOut)
def me(request):
    return request.auth


@auth_router.get("/users", auth=auth, response=list[UserOut])
def list_users(request):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    return list(User.objects.all())


@auth_router.post("/users/{user_id}/toggle-role", auth=auth, response=UserOut)
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


# ── Столики ──────────────────────────────────────────────────────────────────

tables_router = Router(tags=["tables"])


@tables_router.get("/", response=list[TableOut])
def list_tables(request):
    today = datetime.now().date()
    booked_ids = set(
        Booking.objects.filter(
            date=today, status="confirmed"
        ).values_list("table_id", flat=True)
    )
    result = []
    for t in Table.objects.all():
        result.append({
            "id": t.id, "number": t.number, "name": t.name,
            "capacity": t.capacity, "location": t.location,
            "description": t.description, "is_available": t.is_available,
            "is_booked_today": t.id in booked_ids,
        })
    return result


@tables_router.post("/", auth=auth, response=TableOut)
def create_table(request, data: TableIn):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    if Table.objects.filter(number=data.number).exists():
        raise HttpError(400, "Столик с таким номером уже существует")
    return Table.objects.create(**data.dict())


@tables_router.put("/{table_id}", auth=auth, response=TableOut)
def update_table(request, table_id: int, data: TableUpdate):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        raise HttpError(404, "Столик не найден")
    for key, value in data.dict(exclude_none=True).items():
        setattr(table, key, value)
    table.save()
    return table


@tables_router.delete("/{table_id}", auth=auth)
def delete_table(request, table_id: int):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        raise HttpError(404, "Столик не найден")
    table.delete()
    return {"success": True}


# ── Бронирования ─────────────────────────────────────────────────────────────

bookings_router = Router(tags=["bookings"])


@bookings_router.get("/", auth=auth, response=list[BookingOut])
def list_bookings(request):
    qs = Booking.objects.select_related("user", "table")
    if not request.auth.is_staff:
        qs = qs.filter(user=request.auth)
    return list(qs)


@bookings_router.post("/", auth=auth, response=BookingOut)
def create_booking(request, data: BookingIn):
    try:
        table = Table.objects.get(id=data.table_id)
    except Table.DoesNotExist:
        raise HttpError(404, "Столик не найден")

    if not table.is_available:
        raise HttpError(400, "Столик недоступен для бронирования")

    if data.guests_count > table.capacity:
        raise HttpError(400, f"Вместимость столика: {table.capacity} чел.")

    conflict = Booking.objects.filter(
        table=table, date=data.date, status="confirmed"
    ).exists()
    if conflict:
        raise HttpError(409, "Этот столик уже занят на выбранную дату")

    booking = Booking.objects.create(
        user=request.auth,
        table=table,
        date=data.date,
        start_time=data.start_time,
        guests_count=data.guests_count,
        comment=data.comment,
        status="confirmed",
    )
    return Booking.objects.select_related("user", "table").get(id=booking.id)


@bookings_router.delete("/{booking_id}", auth=auth)
def cancel_booking(request, booking_id: int):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        raise HttpError(404, "Бронирование не найдено")
    if not request.auth.is_staff and booking.user != request.auth:
        raise HttpError(403, "Нет прав для отмены этого бронирования")
    booking.status = "cancelled"
    booking.save()
    return {"success": True}
