from django.core.management.base import BaseCommand
from accounts.models import SerialKey

class Command(BaseCommand):
    help = 'توليد مفاتيح تفعيل'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=1)

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            key = SerialKey.objects.create()
            self.stdout.write(self.style.SUCCESS(f'✅ {key.key}'))
