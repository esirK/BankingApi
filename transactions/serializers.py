from rest_framework import serializers
from rest_framework import status
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['amount', 'performed_on']

    def create(self, validated_data):
        self.account = validated_data.get('performed_on')
        self.performed_by = self.context.get('request').user
        self.amount = validated_data.get('amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(detail="Amount must be greater than zero",
                                              code=status.HTTP_400_BAD_REQUEST)
        return value


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

        if self.performed_by.is_customer:
            # ensure it is the owner of the account
            if self.account.owner != self.performed_by:
                raise serializers.ValidationError(detail='You do not have permission to perform this action.',
                                                  code=status.HTTP_403_FORBIDDEN)

        if self.amount > self.account.balance:
            raise serializers.ValidationError(detail='You do not have enough balance to perform this action.')

        self.account.balance -= self.amount
        self.account.save()

        transaction = Transaction.objects.create(type="WITHDRAW",
                                                 amount=self.amount,
                                                 performed_on=self.account,
                                                 performed_by=self.performed_by)
        return transaction

    def to_representation(self, instance):
        return {'type': instance.type, 'performed_by': instance.performed_by.email, 'amount':instance.amount}