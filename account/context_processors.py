from .models import Wallet


def wallet_details(request):
    try:
        wallet = Wallet.objects.get(user=request.user.pk)
    except Wallet.DoesNotExist:
        return {'bonus': 0.00, 'balance': 0.00}

    return {'bonus': wallet.bonus_balance, 'balance': wallet.balance}
