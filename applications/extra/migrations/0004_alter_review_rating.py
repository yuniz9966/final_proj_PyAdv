# Generated by Django 5.2.1 on 2025-05-27 16:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extra', '0003_alter_review_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(help_text='Оценка от 1 до 5', validators=[django.core.validators.MinValueValidator(1, message='Рейтинг должен быть не менее 1.'), django.core.validators.MaxValueValidator(5, message='Рейтинг должен быть не более 5.')], verbose_name='Рейтинг'),
        ),
    ]
