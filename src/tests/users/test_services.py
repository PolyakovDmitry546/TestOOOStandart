from django.contrib.auth.models import User
from django.test import TestCase
from users.models import UserRole

from users.services import UserService


class TestUserService(TestCase):
    def test_add_role(self):
        service = UserService()
        user = User.objects.create_user('user')
        admin = User.objects.create_user('admin')

        service.add_role(user, UserRole.USER)
        service.add_role(admin, UserRole.ADMIN)
        user_role = UserRole.objects.get(user=user)
        admin_role = UserRole.objects.get(user=admin)

        self.assertEqual(user_role.role, UserRole.USER)
        self.assertEqual(admin_role.role, UserRole.ADMIN)

    def test_add_incorrect_role(self):
        service = UserService()
        user = User.objects.create_user('user')

        with self.assertRaises(Exception):
            service.add_role(user, 'sdsd')
