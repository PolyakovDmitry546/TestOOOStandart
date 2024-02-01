from django.urls import path

from api.v1.payments.views import CreateInvoiceAPIView


urlpatterns = [
    path(
        'invoices/create_invoice/',
        CreateInvoiceAPIView.as_view(),
        name='create-invoice-api-view'
    ),
]
