# Generated by Django 5.0.7 on 2024-07-30 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'статья', 'verbose_name_plural': 'статьи'},
        ),
        migrations.RenameField(
            model_name='article',
            old_name='name',
            new_name='title',
        ),
    ]
