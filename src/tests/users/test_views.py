from django.test import TestCase
from django.urls import reverse

from users.models import UserRole
from users.services import UserService


class TestRegisterView(TestCase):
    def test_add_role_to_user_during_registration(self):
        username = 'user'
        password = '12345hgtyiu'

        self.client.post(reverse('register-view'), data={
            'username': username,
            'password1': password,
            'password2': password
        })
        user_roles = UserRole.objects.all()

        self.assertEqual(user_roles.count(), 1)
        self.assertEqual(user_roles[0].role, UserRole.USER)
        self.assertEqual(user_roles[0].user.username, username)

