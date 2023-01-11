from django.core.management.base import BaseCommand
from card.models import Card, Person
from string import ascii_letters
from random import choice
from random import randint
from card.utils import generate_card_number

def create_name():
    abc = ascii_letters
    name = ""
    for iter in range(randint(4, 10)):
        name += choice(abc)
    return name


# класс для создания карт
class Command(BaseCommand):
    help = 'Create cards'

    def handle(self, *args, **options):
        if Card.objects.count() == 0:
            for iteration in range(20):
                person = Person.objects.create(
                    first_name=create_name(),
                    last_name=create_name(),
                )
                Card.objects.create(
                    owner=person,
                    number=generate_card_number(),
                    status="activated",
                    payment_system="visa",
                    card_category="debit",
                    amount=50,
                    cvv=000,
                    pin=000
                )
            self.stdout.write(self.style.SUCCESS('Карты созданы'))
        else:
            self.stdout.write(self.style.WARNING('Уже есть созданные карты'))
