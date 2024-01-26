from rest_framework import serializers

from payments.models import Requisite


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = '__all__'


class RequisiteAjaxResponseSerializer(serializers.Serializer):
    object_list = RequisiteSerializer(many=True)
    page = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previos = serializers.BooleanField()
    has_other_pages = serializers.BooleanField()
    num_pages = serializers.IntegerField()
