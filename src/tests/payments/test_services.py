from decimal import Decimal
from django.test import TestCase
from payments.models import Invoice, Requisite

from payments.services import InvoiceService


class TestInvoiceService(TestCase):
    def test_create_invoice(self):
        expected_amount = Decimal(10)
        expected_invoice_status = Invoice.AWAITING_PAYMENT
        expected_requisite = Requisite.objects.create(
            payment_type=Requisite.CARD,
            card_or_account_type='some type',
            full_name='Some Name',
            phone='81113331122',
            limit=100
        )

        service = InvoiceService()
        (invoice_id, requisite) = service.create_invoice(
            expected_requisite.pk,
            expected_amount
        )
        invocie = Invoice.objects.get(id=invoice_id)

        self.assertEqual(invocie.amount, expected_amount)
        self.assertEqual(invocie.requisite, expected_requisite)
        self.assertEqual(requisite, expected_requisite)
        self.assertEqual(invocie.status, expected_invoice_status)

