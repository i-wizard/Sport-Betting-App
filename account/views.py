from django.db.models import F
from django.shortcuts import render, Http404
from django.utils import timezone
from django.views.generic.base import View
from paystackpy import Transaction, Transfer
from paystackpy.misc import Misc
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum

from account.models import Wallet, Deposit, Withdrawal, Authorization
from referral.models import Referral
from users.models import User
from utilities.helper import LargeResultsSetPagination, Mailer
from .accountsSerializers import DepositSerializer, WithdrawalSerializer, WalletSerializer, AuthorizationSerializer


class WithdrawalView(View):
    def get(self, request):
        return render(request, 'account/withdrawal.html')


class WalletView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WalletSerializer

    def get(self, request):
        try:
            queryset = Wallet.objects.get(user=request.user.pk)
        except Wallet.DoesNotExist:
            return Response(data={'non_field_errors': 'Request could not be validated at this time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


def wallet_details(request):
    try:
        wallet = Wallet.objects.get(user=request.user.pk)
    except Wallet.DoesNotExist:
        raise Http404

    context = {
        'wallet': wallet
    }

    return render(request, 'account/index.html', context)


class Deposits(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DepositSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Deposit.objects.filter(wallet__user=self.request.user.pk).order_by('-id')


class AuthorizationsList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AuthorizationSerializer
    pagination_class = None

    def get_queryset(self):
        return Authorization.objects.filter(user=self.request.user.pk).order_by('-id')


class Withdrawals(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WithdrawalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Withdrawal.objects.filter(wallet__user=self.request.user.pk).order_by('-id')


class ChargeAccount(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            amount = float(request.data.get('amount'))
        except ValueError:
            return Response(
                data={'non_field_errors': 'Please enter valid amount.'},
                status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('authorization_code'):
            return Response(
                data={'response': 'Please enter your account number.'},
                status=status.HTTP_400_BAD_REQUEST)

        authorization_code = request.data.get('authorization_code')
        amount_kobo = amount * 100
        transaction = Transaction()
        response = transaction.charge(request.user.email, auth_code=authorization_code, amount=amount_kobo)

        wallet = Wallet.objects.get(user=request.user.pk)
        deposit = Deposit.objects.create(wallet=wallet, amount=amount,
                                         transaction_uid=response[3]['reference'])

        if response[3]['status'] == 'success':
            deposit.is_confirmed = True
            wallet.balance = F('balance') + amount
            wallet.save()
        else:
            deposit.is_confirmed = False
        deposit.save()

        if not deposit.is_confirmed:
            return Response(data={'response': response[3]['gateway_response']}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=True,
                        status=status.HTTP_200_OK)


class VerifyPayment(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if not request.data.get('ref_id', None):
            return Response(data={'non_field_errors': 'Reference id not valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction()
        response = transaction.verify(request.data.get('ref_id'))

        if response[1]:
            amount = float(response[3]['amount']) / 100

            wallet = Wallet.objects.get(user=request.user.pk)
            deposit = Deposit.objects.create(wallet=wallet, amount=amount,
                                             transaction_uid=response[3]['reference'])
            if response[3]['status'] == 'success':
                deposit.is_confirmed = True
                wallet.balance = F('balance') + amount
                wallet.save()
            elif response[3]['status'] == 'failed':
                deposit.is_confirmed = False
            elif response[3]['status'] == 'abandoned':
                deposit.is_confirmed = False
            deposit.save()

            if deposit.is_confirmed:
                print(response[3]['authorization'])
                authorization_code = response[3]['authorization']['authorization_code']
                last4 = response[3]['authorization']['last4']
                bank = response[3]['authorization']['bank']
                Authorization.objects.get_or_create(authorization_code=authorization_code,
                                                    defaults={'user': request.user, 'bank': bank, 'last4': last4})

            # if request.user.referred:
            #     referral = Referral.objects.get(user=request.user.pk)
            #     if not referral.is_settled:
            #         referral.is_settled = True
            #         referral.save(update_fields=('is_settled',))
            # 
            #         referrer_wallet = Wallet.objects.get(user=referral.referrer.pk)
            #         referrer_wallet.bonus_balance = F('bonus_balance') + 200
            #         referrer_wallet.save(update_fields=('bonus_balance',))
            # 
            #         mailing = Mailer()
            #         mailing.send_referrer_winner(referral.referrer, request.user.username)

            return Response(data={'status': response[3]['status'], 'reference_id': response[3]['reference']},
                            status=status.HTTP_200_OK)

        return Response(data={'non_field_errors': 'Request not valid. please reload and try again or contact support'},
                        status=status.HTTP_400_BAD_REQUEST)


class BanksList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        transaction = Transaction()
        response = transaction.banks()

        if response[0]:
            return Response(data=response[3], status=status.HTTP_200_OK)

        return Response(data=[],
                        status=status.HTTP_200_OK)


class VerifyPassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if not request.data.get('password') or len(request.data.get('password')) < 1:
            return Response(
                data={'response': 'Please enter your password to edit withdrawal details.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=request.user.pk)
        except User.DoesNotExist:
            return Response(
                data={'response': 'Request could not be validated.'},
                status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password').lower()

        if user.check_password(password):
            return Response(
                data={'response': True},
                status=status.HTTP_200_OK)
        return Response(
            data={'response': 'Password does not match.'},
            status=status.HTTP_400_BAD_REQUEST)


class MakeWithdrawal(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if not request.data.get('bank_code'):
            return Response(
                data={'response': 'Request could not be validated please reload and try again.'},
                status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('bank_name') or len(request.data.get('bank_name')) < 1:
            return Response(
                data={'response': 'Please enter bank name.'},
                status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('account_name') or len(request.data.get('account_name')) < 1:
            return Response(
                data={'response': 'Please enter account holder name.'},
                status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('account_number'):
            return Response(
                data={'response': 'Please enter your account number.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(request.data.get('amount'))
        except ValueError:
            return Response(
                data={'response': 'Please enter valid amount.'},
                status=status.HTTP_400_BAD_REQUEST)

        if amount < 1:
            return Response(
                data={'response': 'Please enter amount.'},
                status=status.HTTP_400_BAD_REQUEST)

        amount = amount * 100
        charge = 0
        koboless_amount = amount / 100

        wallet = Wallet.objects.get(user=request.user.pk)
        amount_check = koboless_amount

        previous_withdrawals = Withdrawal.objects.filter(request_at__date=timezone.now().date(),
                                                         wallet=wallet.pk).aggregate(Sum('amount'))
        if previous_withdrawals['amount__sum'] is not None:
            amount_check = float(previous_withdrawals['amount__sum']) + koboless_amount

        if amount_check > 50000:
            return Response(
                data={'response': 'Maximum withdrawal per day is NGN 50,000.'},
                status=status.HTTP_400_BAD_REQUEST)

        if koboless_amount < 1000:
            charge = 50

        koboless_amount = amount / 100
        amount -= (charge * 100)

        if wallet.balance >= koboless_amount:
            balance = Misc().balance()[3][0]['balance']

            if balance > amount:
                withdraw = Transfer()
                create_recipient = withdraw.create_transfer_recipient(name=request.data.get('account_name'),
                                                                      account_number=request.data.get('account_number'),
                                                                      bank_code=request.data.get('bank_code'),
                                                                      currency='NGN')
                if create_recipient[1]:
                    wallet.bank_name = request.data.get('bank_name')
                    wallet.bank_code = request.data.get('bank_code')
                    wallet.bank_account_name = request.data.get('account_name')
                    wallet.bank_account_number = request.data.get('account_number')
                    wallet.save(update_fields=('bank_name', 'bank_code', 'bank_account_name', 'bank_account_number',))

                    response = withdraw.initiate(source='balance', amount=amount, currency='NGN',
                                                 recipient=create_recipient[3]['recipient_code'])
                    # print(response)
                    if response[1]:
                        withdrawal = Withdrawal.objects.create(wallet=wallet, amount=koboless_amount,
                                                               bank_name=request.data.get('bank_name'),
                                                               bank_account_name=request.data.get('account_name'),
                                                               bank_account_number=request.data.get('account_number'),
                                                               transaction_uid=response[3]['transfer_code'])

                        if response[3]['status'] == 'success':
                            withdrawal.transaction_status = 1
                            withdrawal.is_confirmed = True

                            wallet.balance = F('balance') - koboless_amount
                            wallet.save()
                        elif response[3]['status'] == 'pending':
                            withdrawal.transaction_status = 0
                            wallet.balance = F('balance') - koboless_amount
                            wallet.save()
                        elif response[3]['status'] == 'failed':
                            withdrawal.transaction_status = 2
                            withdrawal.is_confirmed = False

                        withdrawal.save()

                        return Response(
                            data={'response': 'Withdrawal request sent.'},
                            status=status.HTTP_200_OK)
                    else:
                        return Response(
                            data={'response': 'Request could not be validated please reload and try again.'},
                            status=status.HTTP_400_BAD_REQUEST)

                return Response(
                    data={'response': create_recipient[2]},
                    status=status.HTTP_400_BAD_REQUEST)

            mailer = Mailer()
            mailer.notify_balance(amount, request.user.username)
            return Response(
                data={'response': 'Request could not be validated please reload and try again.'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={'response': 'You cannot withdraw more than what you have in your balance.'},
            status=status.HTTP_400_BAD_REQUEST)
