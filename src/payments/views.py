from collections.abc import Sequence
from typing import Any

from django.db.models.query import QuerySet
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.generic.list import ListView

from payments.models import Invoice, Requisite
from payments.serializers import RequisiteAjaxResponseSerializer
from payments.services import RequisiteService
from payments.utils import (
    get_requisite_table_headers,
    get_requisite_model_fields,
)


class InvoiceListView(ListView):
    model = Invoice
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        return Invoice.objects.all().order_by('id').select_related('requisite')


class RequisiteListView(ListView):
    model = Requisite
    paginate_by = 50
    ordering = 'id'
    service = RequisiteService()

    def validate_query_params(self):
        ordering = self.request.GET.get('ordering')
        if ordering is not None:
            if len(ordering) > 0 and ordering[0] == '-':
                ordering = ordering[1:]
            if ordering not in get_requisite_model_fields():
                raise ValidationError(
                    f'Incorrect ordering parameter: ordering={ordering}'
                )
        search_field = self.request.GET.get('search_field')
        if search_field is not None and \
                search_field not in get_requisite_model_fields():
            raise ValidationError(
                f'Incorrect search_field parameter: search_field={search_field}'
            )

    def get(self, request, *args, **kwargs) -> HttpResponse:
        try:
            self.validate_query_params()
        except ValidationError as e:
            return HttpResponseNotFound(content=e.message)

        if self.is_ajax():
            context = self.get_context_data(object_list=self.get_queryset())
            response_data = self.service.get_ajax_response(context)
            serializer = RequisiteAjaxResponseSerializer(response_data)
            return JsonResponse(serializer.data, safe=False)

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_field = self.get_search_field()
        search_value = self.get_search_value()
        query = super().get_queryset()
        if search_field is None or search_value is None:
            return query

        search_field += "__icontains"
        query_kwargs = {search_field: search_value}
        query = query.filter(**query_kwargs)
        return query

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ordering'] = self.get_ordering()
        context['table_headers'] = get_requisite_table_headers()

        search_field = self.get_search_field()
        if search_field is not None:
            context['search_field'] = search_field

        search_value = self.get_search_value()
        if search_value is not None:
            context['search_value'] = self.get_search_value()

        return context

    def get_ordering(self) -> Sequence[str]:
        ordering = self.request.GET.get('ordering', self.ordering)
        return ordering

    def get_search_field(self) -> str | None:
        return self.request.GET.get('search_field')

    def get_search_value(self) -> str | None:
        return self.request.GET.get('search_value')

    def is_ajax(self) -> bool:
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'
