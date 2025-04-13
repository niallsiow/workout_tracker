from django.conf import settings
from django.utils.formats import date_format
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from datetime import date

from .models import Session


class HomePageTests(TestCase):
    def test_url_exists_at_correct_location_homepageview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")


class SessionFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        cls.session = Session.objects.create(user=cls.user, notes="some notes")

    def test_model_content(self):
        test_session = Session.objects.last()
        self.assertEqual(test_session.user.username, "testuser")
        self.assertEqual(test_session.user.email, "testuser@email.com")
        self.assertEqual(test_session.notes, "some notes")

    def test_session_createview(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("home"))
        self.assertContains(response, "New Session")

        response = self.client.post(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("session_detail", kwargs={"pk": Session.objects.last().id}),
        )
        self.assertEqual(Session.objects.last().date, date.today())

    def test_session_updateview(self):
        self.client.login(username="testuser", password="testpass123")
        session = Session.objects.last()

        response = self.client.get(reverse("session_detail", kwargs={"pk": session.id}))
        self.assertContains(response, "Edit Notes")

        response = self.client.get(reverse("session_edit", kwargs={"pk": session.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "session_edit.html")
        self.assertContains(response, "some notes")

        response = self.client.post(
            reverse("session_edit", kwargs={"pk": session.id}),
            {"notes": "edited notes"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("session_detail", kwargs={"pk": session.id})
        )
        session = Session.objects.last()
        self.assertEqual(session.notes, "edited notes")

        response = self.client.get(reverse("session_detail", kwargs={"pk": session.id}))
        self.assertContains(response, "edited notes")

    def test_session_deleteview(self):
        self.client.login(username="testuser", password="testpass123")
        new_session = Session.objects.create(user=self.user, notes="new notes")
        self.assertTrue(Session.objects.filter(id=new_session.id).exists())

        response = self.client.get(
            reverse("session_delete", kwargs={"pk": new_session.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "session_delete.html")

        response = self.client.post(
            reverse("session_delete", kwargs={"pk": new_session.id})
        )
        self.assertFalse(Session.objects.filter(id=new_session.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))


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
        self.assertContains(
            response, date_format(date.today(), format=settings.DATE_FORMAT)
        )
        self.assertContains(response, "some notes")
