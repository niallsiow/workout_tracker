from django.urls import path

from .views import SessionListView, SessionDetailView, SessionUpdateView, SessionDeleteView

urlpatterns = [
    path("", SessionListView.as_view(), name="home"),
    path("<int:pk>/", SessionDetailView.as_view(), name="session_detail"),
    path("<int:pk>/edit/", SessionUpdateView.as_view(), name="session_edit"),
    path("<int:pk>/delete/", SessionDeleteView.as_view(), name="session_delete"),
]