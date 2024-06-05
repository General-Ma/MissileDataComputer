from django.urls import path
from . import views

# agents/
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.create_agent, name="get_agent"),
    path("info/<str:id>", views.get_agent, name="create_agent"),
    path("update/<str:id>", views.patch_agent, name="update_agent"),
    path("delete/<str:id>", views.del_agent, name="delete_agent"),
    path("all", views.get_all_agents,name="get_all_agents")
]