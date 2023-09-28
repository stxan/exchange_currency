from django.db import models
# Create your models here.


class CurrencyRate(models.Model):
    currency_code = models.CharField(max_length=3, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    currency_name = models.CharField(max_length=100, unique=True, default="")

    def __str__(self):
        return self.currency_code
