# Generated by Django 3.2.14 on 2022-07-25 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum_User', '0003_auto_20220725_1714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='votes',
            options={'verbose_name': 'Votes', 'verbose_name_plural': 'Votes'},
        ),
    ]
