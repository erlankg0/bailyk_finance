import datetime
import re  # импортируем модуль для работы с регулярными выражениями

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# Модель базы данных для карт и бонусных карт
# Серия карты
# номер карты
# дата выуска карты
# дата окончания действия карты
# дата использованияД
# сумма
# статус карты (не активирована, активирована, просрочена)

# Владелец карты
# Имя
# Фамилия
from django.utils.text import slugify


class Person(models.Model):
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        help_text='Имя должно состоять из букв и быть не длиннее 50 символов только на латинице',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        help_text='Фамилия должна состоять из букв и быть не длиннее 50 символов только на латинице',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Владелец карты'
        verbose_name_plural = 'Владельцы карт'
        db_table = 'person'


class Card(models.Model):
    STATUS_CHOICES = (
        ('not_activated', 'Не активирована'),
        ('activated', 'Активирована'),
        ('expired', 'Просрочена'),
    )
    PAYMENT_SYSTEM_CHOICES = (
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('mir', 'Мир'),
        ('american_express', 'American Express'),
    )
    CARD_CATEGORY_CHOICES = (
        ('bonus', 'Бонусная'),
        ('credit', 'Кредитная'),
        ('debit', 'Дебетовая'),
    )
    card_category = models.CharField(
        max_length=50,
        verbose_name='Категория карты',
        choices=CARD_CATEGORY_CHOICES,
        default='bonus',
    )
    # Владелец карты
    owner = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name='Владелец карты'
    )
    # Серия карты
    series = models.AutoField(primary_key=True)
    # номер карты
    number = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Номер карты',
        help_text='Номер карты должен состоять из 16 цифр (в админ панели для банковских не применять !)',
        blank=True,
        null=True
    )
    payment_system = models.CharField(
        max_length=20,
        verbose_name='Платежная система',
        choices=PAYMENT_SYSTEM_CHOICES,
        help_text='Выберите платежную систему',
        blank=True,
        null=True
    )

    # дата выуска карты
    date_of_issue = models.DateField(
        verbose_name='Дата выдачи карты',
        auto_now_add=True,  # автоматически заполняется текущей датой
    )
    # дата окончания действия карты (годен 4 год)
    date_of_expiry = models.DateField(
        verbose_name='Дата окончания действия карты',
        auto_now_add=True,
    )
    # дата использования карты при покупке
    date_of_use = models.DateField(
        verbose_name='Дата использования карты',
        auto_now_add=True,  # автоматически заполняется текущей датой
    )
    # сумма
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
        help_text='Сумма должна быть больше 0',
        default=0,
    )
    # статус карты (не активирована, активирована, просрочена)
    status = models.CharField(
        max_length=20,
        verbose_name='Статус карты',
        choices=STATUS_CHOICES,
    )
    cvv = models.CharField(
        max_length=3,
        verbose_name='CVV',
        help_text='CVV должен состоять из 3 цифр',
        blank=True,
        null=True
    )
    pin = models.CharField(
        max_length=4,
        verbose_name='PIN',
        help_text='PIN должен состоять из 4 цифр',
        blank=True,
        null=True
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name='URL',
        unique=True,
        blank=True,
        null=True,
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name='Удаленная карта',
        help_text='Инстина, если карта удалена'
    )

    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'slug': self.number})

    # баланс карты (сумма) не может быть меньше 0
    def clean(self):
        if self.amount < 0:
            raise ValidationError('Сумма не может быть меньше 0')
            # валидация номера карты
            # номер карты должен состоять из 16 цифр
            # могут быть только цифры и пробелы или - между цифрами (по 4 цифры)  1234 5678 9012 3456 или 1234-5678-9012-3456 или 1234567890123456
            # регулярное выражение для проверки номера карты на соответствие формату 1234 5678 9012 3456 или 1234-5678-9012-3456 или 1234567890123456
            pattern = '^[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}$'
            if not re.match(pattern, self.number):
                raise ValidationError('Номер карты должен состоять из 16 цифр')
            # валидация даты окончания действия карты
            # дата окончания действия карты не может быть меньше текущей даты
            if self.date_of_expiry < datetime.date.today():
                raise ValidationError(
                    'Дата окончания действия карты не может быть меньше текущей даты')
            # валидация даты использования карты
            # дата использования карты не может быть меньше текущей даты
            if self.date_of_use < datetime.date.today():
                raise ValidationError(
                    'Дата использования карты не может быть меньше текущей даты')
            # валидация даты использования карты
            # дата использования карты не может быть больше даты окончания действия карты
            if self.date_of_use > self.date_of_expiry:
                raise ValidationError(
                    'Дата использования карты не может быть больше даты окончания действия карты')

    def __str__(self):
        if self.number is not None:
            # возвращает номер карты в формате 1234 5678 9012 3456
            return '-'.join([self.number[i:i + 4] for i in range(0, 16, 4)])
        else:
            return 'Карта без номера'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.number)
        super(Card, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        db_table = 'card'


# модель для хранения истории операций с картами
class CardHistory(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        verbose_name='Карта',
        related_name='card_history',
        blank=True,
        null=True,
    )
    date = models.DateField(
        verbose_name='Дата операции',
        default=datetime.date.today,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
    )
    comment = models.CharField(
        max_length=100,
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'История операций с картой'
        verbose_name_plural = 'История операций с картами'
        db_table = 'card_history'
