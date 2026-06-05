from ninja import Router
from ninja.errors import HttpError
from .models import Table
from .schemas import TableOut, TableIn, TableUpdate
from apps.users.auth import auth

router = Router(tags=["tables"])


@router.get("/", response=list[TableOut])
def list_tables(request):
    return list(Table.objects.all())


@router.post("/", auth=auth, response=TableOut)
def create_table(request, data: TableIn):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    if Table.objects.filter(number=data.number).exists():
        raise HttpError(400, "Столик с таким номером уже существует")
    return Table.objects.create(**data.dict())


@router.put("/{table_id}", auth=auth, response=TableOut)
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


@router.delete("/{table_id}", auth=auth)
def delete_table(request, table_id: int):
    if not request.auth.is_staff:
        raise HttpError(403, "Только для администраторов")
    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        raise HttpError(404, "Столик не найден")
    table.delete()
    return {"success": True}
