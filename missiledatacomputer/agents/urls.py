from django.urls import path
from . import views

# agents/
urlpatterns = [
    path("", views.index, name="index"),
]