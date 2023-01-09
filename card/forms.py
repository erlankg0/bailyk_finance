from django.forms import ModelForm

from card.models import Card
from card.utils import generate_card_number


class CardForm(ModelForm):
    # автоматически добавляет номер карты на поле number
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].initial = str(
            generate_card_number())  # автоматически добавляет номер карты на поле number (для карт) или (для бонусных карт)

    class Meta:
        model = Card
        fields = '__all__'
