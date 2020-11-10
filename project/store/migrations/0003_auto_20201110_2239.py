# Generated by Django 3.1.3 on 2020-11-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20201110_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='retail_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма'),
        ),
    ]
