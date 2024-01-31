from typing import Literal
from django.contrib.auth.models import User

from users.models import UserRole


class UserService:
    def add_role(self, user: User, role: Literal['ADMIN', 'USER']) -> None:
        if role != UserRole.USER and role != UserRole.ADMIN:
            raise ValueError(f'illegal role argument role={role}')
        UserRole.objects.create(user=user, role=role)

    def is_admin(self, user: User) -> bool:
        try:
            user_role = UserRole.objects.get(user=user)
        except UserRole.DoesNotExist:
            return False
        return user_role.role == UserRole.ADMIN

    def get_all_user_roles(self):
        return UserRole.objects.all().order_by('id').select_related('user')
