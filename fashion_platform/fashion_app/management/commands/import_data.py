import json
from django.core.management.base import BaseCommand
from fashion_app.models import Item

class Command(BaseCommand):
    help = 'Import fashion items from JSON file'

    def handle(self, *args, **kwargs):
        with open('fashion_items.json') as f:
            data = json.load(f)
            for item_data in data:
                Item.objects.create(**item_data)
        self.stdout.write(self.style.SUCCESS('Successfully imported items'))