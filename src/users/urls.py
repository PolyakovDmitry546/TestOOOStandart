from django.urls import include, path

from users.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-view'),
    path('', include("django.contrib.auth.urls"))
]
