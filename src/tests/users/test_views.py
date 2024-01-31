from django.contrib.auth.models import User
from django.conf import settings
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


class TestUserRoleView(TestCase):
    def test_get_all_user_roles_without_login(self):
        expected_url = settings.LOGIN_URL + '?next=/users/user_roles/'

        response = self.client.get(reverse('user-role-list-view'))
        self.assertRedirects(response, expected_url, 302)

    def test_get_all_user_roles_without_admin_role(self):
        user = User.objects.create_user('user')
        self.client.force_login(user)
        response = self.client.get(reverse('user-role-list-view'))

        self.assertEqual(response.status_code, 403)

    def test_get_all_user_roles(self):
        user = User.objects.create_user('user')
        admin = User.objects.create_user('admin')
        UserRole.objects.create(user=user, role=UserRole.USER)
        UserRole.objects.create(user=admin, role=UserRole.ADMIN)
        expected_roles = UserService().get_all_user_roles()

        self.client.force_login(admin)
        response = self.client.get(reverse('user-role-list-view'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['user_role_list'],
                                 expected_roles)
