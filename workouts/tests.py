from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Session


class HomePageTests(TestCase):
    def test_url_exists_at_correct_location_homepageview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")


class SessionDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        cls.session = Session.objects.create(user=cls.user, notes="some notes")

    def test_url_exists_at_correct_location_sessiondetailview(self):
        response = self.client.get("/1/")
        self.assertEqual(response.status_code, 200)

    def test_session_detail_view(self):
        response = self.client.get(
            reverse("session_detail", kwargs={"pk": self.session.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("session_detail.html")
