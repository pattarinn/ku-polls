"""Module for testing authentication"""
from django.contrib.auth import authenticate
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from polls.tests.test_detail_view import create_question


class AuthenticationTests(TestCase):

    def setUp(self):
        """Setup users for testing"""
        self.user1 = User.objects.create_user(username='jack', email='jackemail@mail.com', password='secret')
        self.user1.first_name = "Jack"
        self.user1.last_name = "Smith"
        self.user1.save()

    def test_can_login(self):
        """Test if the user can login"""
        user = authenticate(username='jack', password='secret')
        self.assertTrue(user is not None)
        self.assertTrue(user.is_authenticated)

    def test_detail_page_not_login(self):
        """Cannot get to detail page if not logged in"""
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        # redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_detail_page(self):
        """Get to detail page when logged in"""
        self.client.login(username='jack', password='secret')
        question = create_question(question_text="Future question.", days=0)
        url = reverse('polls:detail', args=(question.id,))
        response = self.client.get(url)
        # redirect to login page
        self.assertEqual(response.status_code, 200)
