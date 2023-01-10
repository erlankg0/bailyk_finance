from django.contrib import admin

from card.forms import CardForm
from card.models import Card, Person, CardHistory


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    form = CardForm
    prepopulated_fields = {'slug': ('number',)}


@admin.register(CardHistory)
class CardHistoryAdmin(admin.ModelAdmin):
    pass
