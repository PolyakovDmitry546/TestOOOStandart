from django.urls import include, path

from users.views import RegisterView, UserRoleListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-view'),
    path('user_roles/', UserRoleListView.as_view(), name='user-role-list-view'),
    path('', include("django.contrib.auth.urls"))
]
