from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, re_path
from django.utils.html import format_html

from .models import Wallet, Deposit, Withdrawal


class WalletAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'balance', 'bonus_balance')
    ordering = ['id']
    actions = ['clear_bonus']

    def clear_bonus(self, request, queryset):
        rows_updated = queryset.update(bonus_balance=0)
        if rows_updated == 1:
            message_bit = "1 bonus account was"
        else:
            message_bit = "%s bonus account were" % rows_updated
        self.message_user(request, "%s successfully cleared." % message_bit)

    clear_bonus.short_description = "Clear bonus account for marked wallets"


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
