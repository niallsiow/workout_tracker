from django.urls import path

from .views import (
    SessionListView,
    SessionDetailView,
    SessionUpdateView,
    SessionDeleteView,
    WorkoutUpdateView,
    WorkoutDeleteView,
    SetCreateView,
    SetUpdateView,
    SetDeleteView,
    ExerciseListView,
    ExerciseCreateView,
    ExerciseUpdateView,
    ExerciseDeleteView,
)

urlpatterns = [
    path("", SessionListView.as_view(), name="home"),
    path("<int:pk>/", SessionDetailView.as_view(), name="session_detail"),
    path("<int:pk>/session_edit/", SessionUpdateView.as_view(), name="session_edit"),
    path(
        "<int:pk>/session_delete/", SessionDeleteView.as_view(), name="session_delete"
    ),
    path("<int:pk>/workout_edit/", WorkoutUpdateView.as_view(), name="workout_edit"),
    path(
        "<int:pk>/workout_delete/", WorkoutDeleteView.as_view(), name="workout_delete"
    ),
    path("<int:workout_id>/set_new/", SetCreateView.as_view(), name="set_new"),
    path("<int:pk>/set_edit/", SetUpdateView.as_view(), name="set_edit"),
    path("<int:pk>/set_delete/", SetDeleteView.as_view(), name="set_delete"),
    path("exercise_list/", ExerciseListView.as_view(), name="exercise_list"),
    path("exercise_new/", ExerciseCreateView.as_view(), name="exercise_new"),
    path("<int:pk>/exercise_edit/", ExerciseUpdateView.as_view(), name="exercise_edit"),
    path("<int:pk>/exercise_delete/", ExerciseDeleteView.as_view(), name="exercise_delete"),
]
