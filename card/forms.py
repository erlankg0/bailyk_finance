from django.forms import ModelForm

from card.models import Card, Person
from card.utils import generate_card_number


class CardForm(ModelForm):
    # автоматически добавляет номер карты на поле number
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].initial = str(
            generate_card_number())  # автоматически добавляет номер карты на поле number (для карт) или (для бонусных карт)
        # циклом перебираем все поля и добавляем классы в Label
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    class Meta:
        model = Card
        fields = '__all__'


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name',)
