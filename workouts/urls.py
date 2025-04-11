from django.urls import path

from .views import SessionListView, SessionDetailView

urlpatterns = [
    path("", SessionListView.as_view(), name="home"),
    path("<int:pk>/", SessionDetailView.as_view(), name="session_detail"),
]