from django.urls import path

from .views import SessionListView, SessionDetailView, SessionUpdateView

urlpatterns = [
    path("", SessionListView.as_view(), name="home"),
    path("<int:pk>/", SessionDetailView.as_view(), name="session_detail"),
    path("<int:pk>/edit/", SessionUpdateView.as_view(), name="session_edit"),
]