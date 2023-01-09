from django.db import models


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
        return self.first_name

    class Meta:
        verbose_name = 'Владелец карты'
        verbose_name_plural = 'Владельцы карт'
        db_table = 'person'


class BonusCard(models.Model):
    STATUS_CHOICES = (
        ('not_activated', 'Не активирована'),
        ('activated', 'Активирована'),
        ('expired', 'Просрочена'),
    )
    # Владелец карты
    owner = models.ForeignKey(
        'auth.User',
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
        help_text='Номер карты должен состоять из 16 цифр'
    )
    # дата выуска карты
    date_of_issue = models.DateField(
        auto_now_add=True,
        verbose_name='Дата выдачи карты'
    )
    # дата окончания действия карты
    date_of_expiry = models.DateField(
        verbose_name='Дата окончания действия карты'
    )
    # дата использования карты при покупке
    date_of_use = models.DateField(
        verbose_name='Дата использования карты'
    )
    # сумма
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=20,
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

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Бонусная карта'
        verbose_name_plural = 'Бонусные карты'
        db_table = 'bonus_card'


# Банковскя карта
# CVV
# PIN


class Card(BonusCard):
    cvv = models.CharField(
        max_length=3,
        verbose_name='CVV',
        help_text='CVV должен состоять из 3 цифр'
    )
    pin = models.CharField(
        max_length=4,
        verbose_name='PIN',
        help_text='PIN должен состоять из 4 цифр'
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'
        db_table = 'card'
