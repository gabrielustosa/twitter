import pytest

from django.contrib.auth.views import LoginView

from calories.apps.user.views import UserRegisterView
from calories.tests.base import TestCustomBase


@pytest.mark.fast
class AuthViewTest(TestCustomBase):
    def test_register_view_is_correct(self):
        view = self.get_view('register')
        self.assertEqual(view.func.view_class, UserRegisterView)

    def test_register_view_returns_status_code_200(self):
        response = self.response_get('register')
        self.assertEqual(response.status_code, 200)

    def test_register_view_loads_correct_template(self):
        response = self.response_get('register')
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_login_view_is_correct(self):
        view = self.get_view('login')
        self.assertEqual(view.func.view_class, LoginView)

    def test_login_view_returns_status_code_200(self):
        response = self.response_get('login')
        self.assertEqual(response.status_code, 200)

    def test_login_view_loads_correct_template(self):
        response = self.response_get('login')
        self.assertTemplateUsed(response, 'registration/login.html')
