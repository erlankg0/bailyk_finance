from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User


# класс для создания суперпользователя

class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'erlan',
                'era.ab.02@gmail.com',
                '123321',
            )  # создаем суперпользователя
            self.stdout.write(self.style.SUCCESS('Супер пользователь создан'))
        else:
            self.stdout.write(self.style.WARNING('Уже есть такой супер пользователь'))
