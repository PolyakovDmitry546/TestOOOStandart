from collections.abc import Sequence
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from payments.models import Invoice, Requisite
from payments.utils import TableHeader, get_requisite_table_headers


class InvoiceListView(ListView):
    model = Invoice
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        return Invoice.objects.all().order_by('id').select_related('requisite')


class RequisiteListView(ListView):
    model = Requisite
    paginate_by = 50
    ordering = 'id'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ordering'] = self.get_ordering()
        context['table_headers'] = get_requisite_table_headers()
        return context

    def get_ordering(self) -> Sequence[str]:
        ordering = self.request.GET.get('ordering')
        return ordering
