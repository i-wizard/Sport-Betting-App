from django.db import models

from users.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    balance = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    bonus_balance = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    withdrawals = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    withdrawal_code = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_code = models.CharField(max_length=50, null=True, blank=True)
    bank_account_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Deposit(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=17, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    transaction_uid = models.CharField(max_length=20, null=True, blank=True)
    request_at = models.DateTimeField(auto_now_add=True)


class Withdrawal(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=17, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    transaction_uid = models.CharField(max_length=20, null=True, blank=True)
    transaction_status = models.SmallIntegerField(default=0)  # 0 = pending, 1 = success, 2 canceled
    bank_name = models.CharField(max_length=200, blank=True)
    bank_account_name = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=200, blank=True)
    request_at = models.DateTimeField(auto_now_add=True)


class Authorization(models.Model):
    authorization_code = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    bank = models.CharField(max_length=200)
    last4 = models.CharField(max_length=10)
