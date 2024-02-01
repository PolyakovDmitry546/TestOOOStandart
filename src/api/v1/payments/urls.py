from django.urls import path

from api.v1.payments.views import CreateInvoiceAPIView, GetInvoiceStatusAPIView


urlpatterns = [
    path(
        'invoices/create_invoice/',
        CreateInvoiceAPIView.as_view(),
        name='create-invoice-api-view'
    ),
    path(
        'invoices/get_invoice_status/',
        GetInvoiceStatusAPIView.as_view(),
        name='get-invoice-status-api-view'
    )
]
