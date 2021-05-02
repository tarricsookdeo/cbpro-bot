from django.contrib import admin
from .models import Trade


class TradeAdmin(admin.ModelAdmin):
    models = Trade
    list_display = ['ticker', 'shares', 'entry_price',
                    'exit_price', 'entry_datetime',
                    'exit_datetime', 'filled', 'entry_price', 'exit_price']


admin.site.register(Trade, TradeAdmin)
