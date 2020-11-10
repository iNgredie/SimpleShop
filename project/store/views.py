from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from store.models import StoreUser, Product, ShoppingCart
from store.serializers import StoreUserSerializer, ProductSerializer, ShoppingCartSerializer


class StoreUserViewSet(ModelViewSet):
    queryset = StoreUser.objects.all()
    serializer_class = StoreUserSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # корзина доступна на просмотр и редактирование
        # только клиенту-владельцу и любому менеджеру (и админу)
        if self.request.user.is_manager or self.request.user.is_superuser:
            return ShoppingCart.objects.all()
        else:
            return ShoppingCart.objects.filter(
                client=self.request.user
            )

