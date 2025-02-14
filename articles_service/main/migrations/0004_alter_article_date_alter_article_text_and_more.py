# Generated by Django 5.0.7 on 2024-08-03 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_article_text_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата добавления'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.CharField(blank=True, max_length=10000, verbose_name='текст'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, max_length=100, verbose_name='название'),
        ),
    ]
