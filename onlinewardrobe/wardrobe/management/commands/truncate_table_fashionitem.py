from django.core.management.base import BaseCommand, CommandError
from wardrobe.models import FashionItem

class Command(BaseCommand):
    help = 'Truncate a specific table'

    def handle(self, *args, **options):
        try:
            # Delete all FashionItem instances using Django ORM
            FashionItem.objects.all().delete()

            self.stdout.write(self.style.SUCCESS(f'Table {FashionItem._meta.db_table} has been truncated and primary key reset.'))
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
