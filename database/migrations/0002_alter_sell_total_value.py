# Generated by Django 5.1 on 2024-08-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='total_value',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
    ]