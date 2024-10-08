# Generated by Django 5.1 on 2024-09-02 21:21

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Indústria',
                'verbose_name_plural': 'Indústrias',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Setor',
                'verbose_name_plural': 'Setores',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=100)),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('volume', models.BigIntegerField(blank=True, null=True)),
                ('dividend_yield', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.industry')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.sector')),
            ],
            options={
                'verbose_name': 'Ativo',
                'verbose_name_plural': 'Ativos',
            },
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unitary_value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=11)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.stock')),
            ],
            options={
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
            },
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unitary_value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=11)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.stock')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
    ]
