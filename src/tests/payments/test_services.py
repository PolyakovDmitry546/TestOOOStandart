from decimal import Decimal
from django.test import TestCase
from payments.models import Invoice, Requisite

from payments.services import InvoiceService


class TestInvoiceService(TestCase):
    def setUp(self) -> None:
        self.requisite = Requisite.objects.create(
            payment_type=Requisite.CARD,
            card_or_account_type='some type',
            full_name='Some Name',
            phone='81113331122',
            limit=100
        )
        return super().setUp()

    def test_create_invoice(self):
        expected_amount = Decimal(10)
        expected_invoice_status = Invoice.AWAITING_PAYMENT
        expected_requisite = self.requisite

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

    def test_get_invoice_status(self):
        expected_amount = Decimal(10)
        expected_invoice_status = Invoice.AWAITING_PAYMENT
        service = InvoiceService()
        (invoice_id, _) = service.create_invoice(
            self.requisite.pk,
            expected_amount
        )
        invoice_status = service.get_invoice_status(invoice_id)

        self.assertEqual(invoice_status, expected_invoice_status)

    def test_get_invoice_status_with_incorrect_id(self):
        service = InvoiceService()
        service.create_invoice(self.requisite.pk, 5)
        with self.assertRaises(ValueError):
            service.get_invoice_status(3)
