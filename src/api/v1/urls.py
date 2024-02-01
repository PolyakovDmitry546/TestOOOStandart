from django.urls import path, include


urlpatterns = [
    path('payments/', include('api.v1.payments.urls'))
]
