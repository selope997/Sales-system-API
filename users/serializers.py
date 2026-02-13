from rest_framework import serializers
from django.contrib.auth.models import User 


class StoreTotalSalesSerializer(serializers.Serializer):
    """Serializes aggregated total sales per store."""
    store_id = serializers.IntegerField(source='store__id')
    store_name = serializers.CharField(source='store__name')
    total_sales = serializers.DecimalField(max_digits=14, decimal_places=2)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
