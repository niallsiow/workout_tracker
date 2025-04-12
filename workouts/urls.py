from django.urls import path

from .views import SessionListView, SessionDetailView, SessionUpdateView, SessionDeleteView, WorkoutUpdateView, WorkoutDeleteView

urlpatterns = [
    path("", SessionListView.as_view(), name="home"),
    path("<int:pk>/", SessionDetailView.as_view(), name="session_detail"),
    path("<int:pk>/edit_session/", SessionUpdateView.as_view(), name="session_edit"),
    path("<int:pk>/delete_session/", SessionDeleteView.as_view(), name="session_delete"),
    path("<int:pk>/edit_workout/", WorkoutUpdateView.as_view(), name="workout_edit"),
    path("<int:pk>/delete_workout/", WorkoutDeleteView.as_view(), name="workout_delete"),
]