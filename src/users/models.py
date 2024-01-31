from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    "Модель ролей пользователей(пользователь/администратор)"
    USER = 'USER'
    ADMIN = 'ADMIN'
    USER_ROLES = {
        USER: 'Пользователь',
        ADMIN: 'Администратор'
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=5,
        choices=USER_ROLES,
        verbose_name='Роль пользователя'
    )

    class __Meta__:
        db_table = 'user_roles'
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
