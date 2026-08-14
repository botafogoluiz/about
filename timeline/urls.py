from django.urls import path

from . import views

app_name = "timeline"
urlpatterns = [
    path("", views.timeline_home, name="home"),
]
