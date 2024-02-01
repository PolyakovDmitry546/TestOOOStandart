from decimal import Decimal

from django.core.paginator import Page

from payments.models import Invoice, Requisite


class RequisiteService:
    def get_ajax_response(self, context):
        page_obj: Page = context['page_obj']
        response_data = {
            'object_list': page_obj.object_list,
            'page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previos': page_obj.has_previous(),
            'has_other_pages': page_obj.has_other_pages(),
            'num_pages': page_obj.paginator.num_pages,
        }
        return response_data


class InvoiceService:
    def create_invoice(self, requisite_id: int, amount: Decimal) -> tuple[int, Requisite]:
        try:
            requisite = Requisite.objects.get(id=requisite_id)
        except Requisite.DoesNotExist:
            raise ValueError(f'Requisite with id={requisite_id} does not exist')
        invoice = Invoice(
            requisite=requisite,
            amount=amount,
            status=Invoice.AWAITING_PAYMENT
        )
        invoice.save()
        invoice_id = invoice.pk

        return (invoice_id, requisite)

    def get_invoice_status(self, invoice_id: int) -> str:
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise ValueError(f'Invoice with id={invoice_id} does not exist')
        return invoice.status
