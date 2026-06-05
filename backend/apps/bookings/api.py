from ninja import Router
from ninja.errors import HttpError
from django.db.models import Q
from .models import Booking
from .schemas import BookingIn, BookingOut
from apps.users.auth import auth
from apps.tables.models import Table

router = Router(tags=["bookings"])


@router.get("/", auth=auth, response=list[BookingOut])
def list_bookings(request):
    qs = Booking.objects.select_related("user", "table")
    if not request.auth.is_staff:
        qs = qs.filter(user=request.auth)
    return list(qs)


@router.post("/", auth=auth, response=BookingOut)
def create_booking(request, data: BookingIn):
    try:
        table = Table.objects.get(id=data.table_id)
    except Table.DoesNotExist:
        raise HttpError(404, "Столик не найден")

    if not table.is_available:
        raise HttpError(400, "Столик недоступен для бронирования")

    if data.guests_count > table.capacity:
        raise HttpError(400, f"Вместимость столика: {table.capacity} чел.")

    if data.start_time >= data.end_time:
        raise HttpError(400, "Время начала должно быть раньше времени окончания")

    conflict = Booking.objects.filter(
        table=table,
        date=data.date,
        status="confirmed",
    ).filter(
        Q(start_time__lt=data.end_time) & Q(end_time__gt=data.start_time)
    ).exists()

    if conflict:
        raise HttpError(409, "Этот столик уже забронирован на выбранное время")

    booking = Booking.objects.create(
        user=request.auth,
        table=table,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        guests_count=data.guests_count,
        comment=data.comment,
        status="confirmed",
    )
    return Booking.objects.select_related("user", "table").get(id=booking.id)


@router.delete("/{booking_id}", auth=auth)
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
