# Generated by Django 4.2.13 on 2024-06-09 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashc', models.CharField(max_length=200, verbose_name='Хеш')),
                ('url', models.URLField(verbose_name='Ссылка')),
            ],
        ),
    ]
