from django.conf import settings
from django.utils.formats import date_format
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from datetime import date

from .models import Session, Exercise, Workout


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
        cls.session = Session.objects.create(user=cls.user)

    def test_session_model_content(self):
        test_session = Session.objects.last()
        self.assertEqual(test_session.user.username, "testuser")
        self.assertEqual(test_session.user.email, "testuser@email.com")

    def test_session_createview(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("session_detail", kwargs={"pk": Session.objects.last().id}),
        )
        self.assertEqual(Session.objects.last().date, date.today())

    def test_session_deleteview(self):
        self.client.login(username="testuser", password="testpass123")
        new_session = Session.objects.create(user=self.user)
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
        cls.session = Session.objects.create(user=cls.user)

    def test_url_exists_at_correct_location_sessiondetailview(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/1/")
        self.assertEqual(response.status_code, 200)

    def test_session_detail_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("session_detail", kwargs={"pk": self.session.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("session_detail.html")
        self.assertContains(
            response, date_format(date.today(), format=settings.DATE_FORMAT)
        )


class WorkoutFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        cls.session = Session.objects.create(user=cls.user)
        cls.exercise = Exercise.objects.create(user=cls.user, name="Deadlift")
        cls.workout = Workout.objects.create(
            session=cls.session, exercise=cls.exercise, working_weight=100
        )

    def test_workout_model_content(self):
        test_workout = Workout.objects.last()
        self.assertEqual(test_workout.exercise.name, "Deadlift")
        self.assertEqual(test_workout.working_weight, 100)

    def test_workout_createview(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("session_detail", kwargs={"pk": self.session.id}),
            {"exercise": self.exercise.id, "working_weight": 50},
        )
        new_workout = Workout.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("workout_edit", kwargs={"pk": new_workout.id})
        )
        self.assertEqual(new_workout.working_weight, 50)

    def test_workout_updateview(self):
        self.client.login(username="testuser", password="testpass123")
        new_workout = Workout.objects.create(
            session=self.session, exercise=self.exercise, working_weight=10
        )

        response = self.client.get(
            reverse("workout_edit", kwargs={"pk": new_workout.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workout_edit.html")
        self.assertContains(response, "10")

        response = self.client.post(
            reverse("workout_edit", kwargs={"pk": new_workout.id}),
            {
                "exercise": self.exercise.id,
                "working_weight": 25,
                "next_weight": 1,
                "next_sets": 1,
                "next_reps": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("workout_edit", kwargs={"pk": new_workout.id})
        )
        edited_workout = Workout.objects.get(id=new_workout.id)
        self.assertEqual(edited_workout.working_weight, 25)

    def test_workout_deleteview(self):
        self.client.login(username="testuser", password="testpass123")
        new_workout = Workout.objects.create(
            session=self.session, exercise=self.exercise, working_weight=30
        )
        self.assertTrue(Workout.objects.filter(id=new_workout.id).exists())

        response = self.client.get(
            reverse("workout_delete", kwargs={"pk": new_workout.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workout_delete.html")

        response = self.client.post(
            reverse("workout_delete", kwargs={"pk": new_workout.id})
        )
        self.assertFalse(Workout.objects.filter(id=new_workout.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("session_detail", kwargs={"pk": new_workout.session.id})
        )
