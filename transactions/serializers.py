from rest_framework import serializers
from rest_framework import status
from .models import Transaction

from accounts.models import CustomerBankAccount


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('amount', 'performed_on')

    def create(self, validated_data):
        self.account = validated_data.get('performed_on')
        self.performed_by = self.context.get('request').user
        self.amount = validated_data.get('amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(detail="Amount must be greater than zero",
                                              code=status.HTTP_400_BAD_REQUEST)
        return value

    def verify_owner(self):
        if self.performed_by.is_customer:
            # ensure it is the owner of the account
            if self.account.owner != self.performed_by:
                raise serializers.ValidationError(detail='You do not have permission to perform this action.',
                                                  code=status.HTTP_403_FORBIDDEN)

    def check_balance(self):
        if self.amount > self.account.balance:
            raise serializers.ValidationError(detail='You do not have enough balance to perform this action.')


class TopUpSerializer(TransactionSerializer):
    def create(self, validated_data):
        super().create(validated_data)

        self.account.balance += self.amount
        self.account.save()

        transaction = Transaction.objects.create(type="TOP_UP",
                                    amount=self.amount,
                                    performed_on=self.account,
                                    performed_by=self.performed_by)
        return transaction

    def to_representation(self, instance):
        return {'type': instance.type, 'performed_by': instance.performed_by.email, 'amount':instance.amount}


class WithdrawSerializer(TransactionSerializer):
    def create(self, validated_data):
        super().create(validated_data)

        self.verify_owner()
        self.check_balance()

        self.account.balance -= self.amount
        self.account.save()

        transaction = Transaction.objects.create(type="WITHDRAW",
                                                 amount=self.amount,
                                                 performed_on=self.account,
                                                 performed_by=self.performed_by)
        return transaction

    def to_representation(self, instance):
        return {'type': instance.type, 'performed_by': instance.performed_by.email, 'amount':instance.amount}


class TransferSerializer(TransactionSerializer):

    class Meta(TransactionSerializer.Meta):
        fields = TransactionSerializer.Meta.fields + ('transfer_to',)

    def create(self, validated_data):
        super().create(validated_data)

        self.verify_owner()
        self.check_balance()

        self.transfer_to = validated_data.get('transfer_to')

        self.account.balance -= self.amount
        self.transfer_to.balance += self.amount

        self.account.save()
        self.transfer_to.save()

        transaction = Transaction.objects.create(type="TRANSFER",
                                                 amount=self.amount,
                                                 performed_on=self.account,
                                                 performed_by=self.performed_by,
                                                 transfer_to=self.transfer_to
                                                 )
        return transaction

    def to_representation(self, instance):
        return {'type': instance.type, 'performed_by': instance.performed_by.email, 'amount':instance.amount}

    def validate_transfer_to(self, value):
        # Verify we are transferring to a customer bank account
        values = self.get_initial()
        sender = CustomerBankAccount.objects.get(id=values.get('performed_on'))
        receiver = CustomerBankAccount.objects.get(id=values.get('transfer_to'))

        if sender.id == receiver.id:
            # You can not transfer funds to own account
            raise serializers.ValidationError(detail="You can not transfer funds to your own account")

        return value
