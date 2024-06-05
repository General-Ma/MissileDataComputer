from django.urls import path
from . import views

# missile_launchers/
urlpatterns = [
    path("", views.index, name="index"),
]