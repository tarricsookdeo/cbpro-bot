from django.db import models


class Trade(models.Model):
    ticker = models.CharField(max_length=8)
    shares = models.DecimalField(max_digits=14, decimal_places=8)
    entry_price = models.DecimalField(max_digits=13, decimal_places=6)
    exit_price = models.DecimalField(
        max_digits=13, decimal_places=6, null=True, blank=True)
    entry_datetime = models.DateTimeField(null=True, blank=True)
    exit_datetime = models.DateTimeField(null=True, blank=True)
    filled = models.BooleanField(default=False)
    entry_fee = models.DecimalField(max_digits=14, decimal_places=8)
    exit_fee = models.DecimalField(
        max_digits=14, decimal_places=8, null=True, blank=True)
    paper_trade = models.BooleanField(default=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
