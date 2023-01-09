# Generated by Django 4.1.5 on 2023-01-09 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_card_card_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'verbose_name': 'Карта', 'verbose_name_plural': 'Карты'},
        ),
        migrations.AddField(
            model_name='card',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='URL'),
        ),
    ]