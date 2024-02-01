from rest_framework import serializers

from payments.models import Requisite


class CreateInvoiceSerializer(serializers.Serializer):
    requisite_id = serializers.IntegerField(min_value=0)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = '__all__'


class CreateInvoiceOutSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    requisite = RequisiteSerializer()
