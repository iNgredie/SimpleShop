from rest_framework.routers import SimpleRouter

from store.views import StoreUserViewSet, ProductViewSet, ShoppingCartViewSet

urlpatterns = []

router = SimpleRouter()

router.register(r'user', StoreUserViewSet)
router.register(r'product', ProductViewSet)
router.register(r'sc', ShoppingCartViewSet)

urlpatterns += router.urls