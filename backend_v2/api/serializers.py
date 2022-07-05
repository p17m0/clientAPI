from rest_framework import serializers
from .models import *


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        """Contains model & fields used by this serializer."""

        model = Client
        fields = '__all__'


class ClientsOrgSerializer(serializers.ModelSerializer):
    class Meta:
        """Contains model & fields used by this serializer."""

        model = ClientOrg
        fields = '__all__'


class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        """Contains model & fields used by this serializer."""

        model = FileUpload
        fields = '__all__'
