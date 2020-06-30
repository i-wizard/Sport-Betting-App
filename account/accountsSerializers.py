from rest_framework import serializers

from account.models import Deposit, Withdrawal, Wallet, Authorization


class DepositSerializer(serializers.ModelSerializer):
    amount = serializers.CharField()

    class Meta:
        model = Deposit
        fields = ('amount', 'is_confirmed', 'transaction_uid', 'request_at',)

    def validate(self, attrs):
        amount = attrs.get('amount')
        amount = round(float(amount), 2)

        if amount < 200:
            raise serializers.ValidationError("Deposit Amount must be more than 200 naira.")

        if amount > 999999999999999.99:
            raise serializers.ValidationError("Please enter an accurate deposit amount")

        return attrs

    # def create(self, validated_data):


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class AuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorization
        fields = '__all__'
