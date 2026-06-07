from django.urls import path
from ninja import NinjaAPI
from restaurant.api import auth_router, tables_router, bookings_router

api = NinjaAPI(title="Restaurant Booking API", version="1.0.0", docs_url="/docs")

api.add_router("/auth", auth_router)
api.add_router("/tables", tables_router)
api.add_router("/bookings", bookings_router)

urlpatterns = [path("api/", api.urls)]
