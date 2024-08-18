from django.utils.timezone import datetime, timedelta
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Course, Lesson, UserToGroup
from users.models import Balance, CustomUser, Subscription


def create_usual_user():
    user = CustomUser.objects.create_user(
        id=0,
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )

    return user


def create_lessons():
    lesson = Lesson.objects.create(title="test", link="https://test.com", course_id=2)


def create_courses():
    course = Course.objects.create(author="Test", title="Test course", cost=500, start_date=datetime.now())
    course2 = Course.objects.create(author="New", title="New course", cost=1500, start_date=datetime.now() + timedelta(365))
    course3 = Course.objects.create(author="New", title="New course", cost=500, start_date=datetime.now() + timedelta(365))

    create_lessons()
    return course, course2, course3


def get_user_balance(user):
    return Balance.objects.get(user=user)


def get_all_subs(user):
    return Subscription.objects.filter(user=user)


class CoursesApiTest(APITestCase):

    def setUp(self):
        self.user = create_usual_user()
        self.client = APIClient()
        self.course, self.course2, self.course3 = create_courses()
        self.client.force_authenticate(user=self.user)


    def test_pay_for_course(self):
        url = reverse('courses-pay', kwargs={"pk": self.course.pk})
        response = self.client.post(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_balance(self.user).balance, 500)
        self.assertNotEqual(len(get_all_subs(self.user)), 0)
        self.assertEqual(len(UserToGroup.objects.all()),  1)


    def test_get_all_courses(self):
        url = reverse('courses-list')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Course.objects.all()))


    def test_get_non_bought_courses(self):
        url = reverse('courses-pay', kwargs={"pk": self.course3.pk})
        response = self.client.post(url, format="json")

        url = reverse('courses-products-for-pay')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
