from django.db import models
from django.core.validators import MinValueValidator

from yfinance import Ticker

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True, db_index=True)
    password = models.CharField(max_length=50, null=False, unique=True)
    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})


class Industry(models.Model):
    industry = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Indústria"
        verbose_name_plural = "Indústrias"

    def __str__(self):
        return self.industry

    def get_absolute_url(self):
        return reverse("Industry_detail", kwargs={"pk": self.pk})


class Sector(models.Model):
    sector = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.sector

    def get_absolute_url(self):
        return reverse("Sector_detail", kwargs={"pk": self.pk})


class Stock(models.Model):
    ticker = models.CharField(max_length=4, null=False, unique=True, db_index=True)
    company_name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        ticker_data = Ticker(self.ticker)
        info = ticker_data.info
        self.company_name = info.get("shortName")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"

    def __str__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse("Stock_detail", kwargs={"pk": self.pk})


class Buy(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=False, db_index=True, default=1
    )
    ticker = models.ForeignKey("Stock", on_delete=models.CASCADE, db_index=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    amount = models.PositiveIntegerField(
        null=False,
        validators=[
            MinValueValidator(1),
        ],
    )
    unitary_value = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    total_value = models.DecimalField(max_digits=11, decimal_places=2, null=False)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return self.ticker.ticker

    def get_absolute_url(self):
        return reverse("Buy_detail", kwargs={"pk": self.pk})


class Sell(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=False, db_index=True, default=1
    )
    ticker = models.ForeignKey("Stock", on_delete=models.CASCADE, db_index=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    amount = models.PositiveIntegerField(
        null=False,
        validators=[
            MinValueValidator(1),
        ],
    )
    unitary_value = models.DecimalField(max_digits=3, decimal_places=2, null=False)
    total_value = models.DecimalField(max_digits=9, decimal_places=2, null=False)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse("Sell_detail", kwargs={"pk": self.pk})
