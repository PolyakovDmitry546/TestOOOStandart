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

    def test_is_admin(self):
        service = UserService()
        not_admin_user = User.objects.create_user(username='not_admin_user')
        admin_user = User.objects.create_user(username='admin')
        user_without_role = User.objects.create_user(username='anonymus')
        service.add_role(admin_user, UserRole.ADMIN)
        service.add_role(not_admin_user, UserRole.USER)

        self.assertTrue(service.is_admin(admin_user))
        self.assertFalse(service.is_admin(not_admin_user))
        self.assertFalse(service.is_admin(user_without_role))

    def test_get_all_user_roles(self):
        user = User.objects.create_user('user')
        admin = User.objects.create_user('admin')
        UserRole.objects.create(user=user, role=UserRole.USER)
        UserRole.objects.create(user=admin, role=UserRole.ADMIN)
        expected_roles = UserRole.objects.all().order_by('id')

        user_roles = UserService().get_all_user_roles()

        self.assertQuerySetEqual(user_roles,
                                 expected_roles)
