from django.urls import path

from payments.views import InvoiceListView

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice-list-view'),
]
