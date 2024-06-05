from django.urls import path
from . import views

# missiles/
urlpatterns = [
    path("", views.index, name="index"),
]