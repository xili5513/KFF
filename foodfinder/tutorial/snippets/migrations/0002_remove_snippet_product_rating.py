# Generated by Django 2.1.7 on 2019-04-26 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='product_rating',
        ),
    ]