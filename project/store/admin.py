from django.contrib import admin

from store.models import StoreUser, ShoppingCart, Product

admin.site.register(StoreUser)
admin.site.register(ShoppingCart)
admin.site.register(Product)
