from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

import yfinance as yf

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
    industry_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Indústria"
        verbose_name_plural = "Indústrias"

    def __str__(self):
        return self.industry_name

    def get_absolute_url(self):
        return reverse("Industry_detail", kwargs={"pk": self.pk})


class Sector(models.Model):
    sector_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.sector_name

    def get_absolute_url(self):
        return reverse("Sector_detail", kwargs={"pk": self.pk})


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100, blank=True)
    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    market_cap = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    volume = models.BigIntegerField(blank=True, null=True)
    dividend_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    last_updated = models.DateTimeField(auto_now=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey(
        Industry, on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.ticker = self.ticker.upper()

        if Stock.objects.filter(ticker=self.ticker).exists():
            return

        ticker_data = yf.Ticker(self.ticker)
        info = ticker_data.info

        if not info or "shortName" not in info:
            return

        self.company_name = info.get("shortName", "")
        self.current_price = info.get("currentPrice", 0)
        self.market_cap = info.get("marketCap", 0)
        self.volume = info.get("volume", 0)
        self.dividend_yield = (
            info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0
        )

        sector_name = info.get("sector", "Unknown")
        if sector_name:
            sector, created = Sector.objects.get_or_create(sector_name=sector_name)
            self.sector = sector

        industry_name = info.get("industry", "Unknown")
        if industry_name:
            industry, created = Industry.objects.get_or_create(
                industry_name=industry_name
            )
            self.industry = industry

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"

    def __str__(self):
        return f"{self.company_name} ({self.ticker})"

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
    unitary_value = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    total_value = models.DecimalField(max_digits=11, decimal_places=2, null=False)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return self.ticker.ticker

    def get_absolute_url(self):
        return reverse("Sell_detail", kwargs={"pk": self.pk})
