from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.payments.serializers import (CreateInvoiceOutSerializer,
                                         GetInvoiceStatusOutSerializer)
from payments.services import InvoiceService


class CreateInvoiceAPIView(APIView):
    def post(self, request: Request):
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                (invoice_id, requisite) = InvoiceService().create_invoice(
                    **serializer.data
                )
                out_serializer = CreateInvoiceOutSerializer(
                    {
                        'invoice_id': invoice_id,
                        'requisite': requisite
                    }
                )
                return Response(out_serializer.data,
                                status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response(
                    ErrorSerializer({'message': " ".join(e.args)}).data,
                    status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(
                    ErrorSerializer({'message': " "}).data,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {'message': " ".join(serializer.errors)},
                status.HTTP_400_BAD_REQUEST)


class GetInvoiceStatusAPIView(APIView):
    def get(self, request: Request):
        invoice_id = request.query_params.get('invoice_id')
        if invoice_id is None:
            return Response(
                ErrorSerializer(
                    {'message': 'Required parameter invoice_id was not sent'}
                ).data,
                status.HTTP_400_BAD_REQUEST)
        try:
            invoice_status = InvoiceService().get_invoice_status(invoice_id)
            return Response(
                GetInvoiceStatusOutSerializer(
                    {'invoice_status': invoice_status}
                ).data,
                status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                ErrorSerializer({'message': " ".join(e.args)}).data,
                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                ErrorSerializer({'message': " "}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
