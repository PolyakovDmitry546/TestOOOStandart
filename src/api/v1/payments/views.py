from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.payments.serializers import (CreateInvoiceOutSerializer,
                                         CreateInvoiceSerializer)
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
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
