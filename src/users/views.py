from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

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


class UserRoleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserRole
    paginate_by = 50
    template_name = 'users/user_role_list.html'
    context_object_name = 'user_role_list'

    def test_func(self) -> bool:
        return UserService().is_admin(self.request.user)

    def get_queryset(self) -> QuerySet[UserRole]:
        return UserService().get_all_user_roles()
