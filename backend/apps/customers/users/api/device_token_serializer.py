from rest_framework import serializers
from apps.customers.users.models.device_token import DeviceToken

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['token']
