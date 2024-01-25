from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from payments.models import Invoice, Requisite


class InvoiceListView(ListView):
    model = Invoice
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        return Invoice.objects.all().order_by('id').select_related('requisite')


class RequisiteListView(ListView):
    model = Requisite
    paginate_by = 50
