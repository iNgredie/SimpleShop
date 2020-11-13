from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import StoreUser, Product, ShoppingCart


class StoreUserSerializer(ModelSerializer):
    class Meta:
        model = StoreUser
        fields = (
            'id',
            'email',
            'first_name',
            'surname',
            'patronymic',
            'delivery_address',
            'is_manager'
        )


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShoppingCartSerializer(ModelSerializer):
    client_name = serializers.StringRelatedField(
        source='client',
        read_only=True
    )
    product_title = serializers.StringRelatedField(
        source='product',
        read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'client_name',
            'product_title',
            'amount',
            'price',
            'total'
        )


