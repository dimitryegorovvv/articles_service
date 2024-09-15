# Generated by Django 5.0.7 on 2024-08-09 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='комментарий'),
        ),
    ]
