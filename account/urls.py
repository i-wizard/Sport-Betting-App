from django.urls import path

from account.views import WithdrawalView, WalletView, wallet_details, Deposits, Withdrawals, VerifyPayment, BanksList, \
    MakeWithdrawal, VerifyPassword, AuthorizationsList, ChargeAccount
from utilities.general_middleware import AuthCheckMiddleware
from django.utils.decorators import decorator_from_middleware

app_name = 'account'

user_auth_decorator = decorator_from_middleware(AuthCheckMiddleware)

urlpatterns = [
    path('withdrawal', user_auth_decorator(WithdrawalView.as_view()), name='withdrawal'),
    path('wallet', WalletView.as_view()),
    path('', user_auth_decorator(wallet_details), name='details'),
    path('api/deposits', Deposits.as_view()),
    path('api/withdraw', MakeWithdrawal.as_view()),
    path('api/banks', BanksList.as_view()),
    path('api/withdrawals', Withdrawals.as_view()),
    path('payment/verify', VerifyPayment.as_view()),
    path('api/password-check', VerifyPassword.as_view()),
    path('api/authorizations', AuthorizationsList.as_view()),
    path('api/charge', ChargeAccount.as_view()),
]
