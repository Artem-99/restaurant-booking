from django.urls import path
from ninja import NinjaAPI
from apps.users.api import router as auth_router
from apps.tables.api import router as tables_router
from apps.bookings.api import router as bookings_router

api = NinjaAPI(title="Restaurant Booking API", version="1.0.0", docs_url="/docs")

api.add_router("/auth", auth_router)
api.add_router("/tables", tables_router)
api.add_router("/bookings", bookings_router)

urlpatterns = [
    path("api/", api.urls),
]
