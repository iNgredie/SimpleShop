import csv

import requests
from django.core.management import BaseCommand

from store.management.commands.csv_url import url
from store.models import Product


class AddingProducts:

    def get_products(self):
        with requests.get(url, stream=True) as r:
            lines = (line.decode('utf-8') for line in r.iter_lines())
            for row in csv.DictReader(lines, delimiter=';'):
                p_price = int(row['Цена']) * 0.9
                r_price = int(row['Цена']) * 1.2 if int(row['Цена']) < 1000 else int(row['Цена']) * 1.1
                p = Product(
                    vendor_code=row['Код товара'],
                    title=row['Наименование'],
                    purchase_price=p_price,
                    retail_price=r_price
                ).save()


class Command(BaseCommand):
    help = 'Adding products'

    def handle(self, *args, **options):
        script = AddingProducts()
        script.get_products()