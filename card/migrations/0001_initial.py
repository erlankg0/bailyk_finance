# Generated by Django 4.1.5 on 2023-01-09 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Имя должно состоять из букв и быть не длиннее 50 символов только на латинице', max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Фамилия должна состоять из букв и быть не длиннее 50 символов только на латинице', max_length=50, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'Владелец карты',
                'verbose_name_plural': 'Владельцы карт',
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('series', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(blank=True, help_text='Номер карты должен состоять из 16 цифр (в админ панели для банковских не применять !)', max_length=16, null=True, unique=True, verbose_name='Номер карты')),
                ('payment_system', models.CharField(choices=[('visa', 'Visa'), ('mastercard', 'MasterCard'), ('mir', 'Мир'), ('american_express', 'American Express')], help_text='Выберите платежную систему', max_length=20, verbose_name='Платежная система')),
                ('date_of_issue', models.DateField(auto_now_add=True, verbose_name='Дата выдачи карты')),
                ('date_of_expiry', models.DateField(auto_now_add=True, verbose_name='Дата окончания действия карты')),
                ('date_of_use', models.DateField(auto_now_add=True, verbose_name='Дата использования карты')),
                ('amount', models.DecimalField(decimal_places=2, default=0, help_text='Сумма должна быть больше 0', max_digits=10, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('not_activated', 'Не активирована'), ('activated', 'Активирована'), ('expired', 'Просрочена')], max_length=20, verbose_name='Статус карты')),
                ('cvv', models.CharField(help_text='CVV должен состоять из 3 цифр', max_length=3, verbose_name='CVV')),
                ('pin', models.CharField(help_text='PIN должен состоять из 4 цифр', max_length=4, verbose_name='PIN')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.person', verbose_name='Владелец карты')),
            ],
            options={
                'verbose_name': 'Бонусная карта',
                'verbose_name_plural': 'Бонусные карты',
                'db_table': 'bonus_card',
            },
        ),
    ]
