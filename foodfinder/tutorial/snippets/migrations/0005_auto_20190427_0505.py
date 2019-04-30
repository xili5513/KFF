# Generated by Django 2.1.7 on 2019-04-27 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productId', to='snippets.Snippet'),
        ),
    ]