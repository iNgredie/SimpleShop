from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('store.urls')),

    # тут регистрация
    path('api/v1/auth/', include('djoser.urls')),

    # /login тут авторизация
    path('api/v1/', include('rest_framework.urls')),
]
