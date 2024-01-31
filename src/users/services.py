from typing import Literal
from django.contrib.auth.models import User

from users.models import UserRole


class UserService:
    def add_role(self, user: User, role: Literal['ADMIN', 'USER']) -> None:
        if role != UserRole.USER and role != UserRole.ADMIN:
            raise ValueError(f'illegal role argument role={role}')
        UserRole.objects.create(user=user, role=role)

