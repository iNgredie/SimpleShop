from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class StoreUser(AbstractUser):
    """" Custom user model
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )
    email = models.EmailField(
        'email',
        unique=True
    )
    first_name = models.CharField(
        'имя',
        max_length=255
    )
    surname = models.CharField(
        'фамилия',
        max_length=255
    )
    patronymic = models.CharField(
        'отчество',
        max_length=255
    )
    delivery_address = models.CharField(
        'адрес доставки',
        max_length=1000
    )
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.email


class Product(models.Model):
    """" Product model
    """
    vendor_code = models.CharField(
        'артикул',
        max_length=255
    )
    title = models.CharField(
        'наименование',
        max_length=255
    )
    purchase_price = models.DecimalField(
        'закупочная цена',
        max_digits=10,
        decimal_places=2
    )
    retail_price = models.DecimalField(
        'розничная цена',
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return '%s' % self.title


class ShoppingCart(models.Model):
    """" Shopping cart model
    """
    client = models.ForeignKey(
        StoreUser,
        on_delete=models.CASCADE,
        related_name='client'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product'
    )
    amount = models.PositiveIntegerField(
        'количество',
        default=0
    )
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2
    )
    total = models.DecimalField(
        'сумма',
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        # функция рассчитывает сумму в корзине
        self.price = self.product.retail_price
        self.total = self.price * self.amount
        super(ShoppingCart, self).save(*args, **kwargs)

        # если у пользователя есть корзина, новую не создает
        if not self.pk and ShoppingCart.objects.exists():
            raise ValidationError('You already have a shopping cart')
        return super(ShoppingCart, self).save(*args, **kwargs)


    def __str__(self):
        return '%s: %s' % (self.client, self.product)




