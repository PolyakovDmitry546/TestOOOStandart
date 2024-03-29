from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from payments.models import Invoice, Requisite
from payments.services import InvoiceService


class TestCreateInvoiceView(APITestCase):
    def test_create_invoice(self):
        expected_requisite = Requisite.objects.create(
            payment_type=Requisite.CARD,
            card_or_account_type='some type',
            full_name='Some Name',
            phone='81113331122',
            limit=100
        )
        expected_amount = 10
        response = self.client.post(
            path=reverse('create-invoice-api-view'),
            data={
                'requisite_id': expected_requisite.pk,
                'amount': expected_amount
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertIn('invoice_id', response_data)
        self.assertEqual(response_data['requisite']['id'], expected_requisite.pk)

    def test_create_invoice_incorrect_data(self):
        response = self.client.post(
            path=reverse('create-invoice-api-view'),
            data={
                'requisite': 'some_req',
                'some_amount': 123,
                'some_field': '123'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_non_existent_requisite(self):
        response = self.client.post(
            path=reverse('create-invoice-api-view'),
            data={
                'requisite_id': 1,
                'amount': 123,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGetInvoiceStatusView(APITestCase):
    def setUp(self) -> None:
        self.requisite = Requisite.objects.create(
            payment_type=Requisite.CARD,
            card_or_account_type='some type',
            full_name='Some Name',
            phone='81113331122',
            limit=100
        )
        return super().setUp()

    def test_get_invoice_status(self):
        service = InvoiceService()
        (invoice_id, _) = service.create_invoice(self.requisite.pk, 5)
        expected_invoice_status = Invoice.AWAITING_PAYMENT

        response = self.client.get(
            path=reverse('get-invoice-status-api-view'),
            data={'invoice_id': invoice_id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['invoice_status'], expected_invoice_status)

    def test_get_invoice_status_incorrect_data(self):
        response = self.client.get(
            path=reverse('get-invoice-status-api-view'),
            data={'invoice_id': 4}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
