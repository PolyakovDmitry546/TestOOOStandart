from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.models import UserRole
from users.services import UserService


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    success_url = reverse_lazy('requisite-list-view')
    form_class = UserCreationForm

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        service = UserService()
        service.add_role(self.object, UserRole.USER)
        return response
