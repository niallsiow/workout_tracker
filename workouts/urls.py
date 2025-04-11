from django.urls import path

from .views import SessionListView

urlpatterns = [
    path("", SessionListView.as_view(), name="home"),
]