from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SignupPageTests(TestCase):

    def test_signup_page_status_code(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertContains(response, 'Sign Up')

    def test_signup_form_creates_user(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newuser',
                'password1': 'ComplexPass123',
                'password2': 'ComplexPass123',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())
