from django.urls import path

from payments.views import InvoiceListView, RequisiteListView

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice-list-view'),
    path('requisites/', RequisiteListView.as_view(), name='requisite-list-view')
]
