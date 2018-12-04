from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['amount', 'performed_on', 'type']

    def create(self, validated_data):
        self.account = validated_data.get('performed_on')
        self.performed_by = self.context.get('request').user
        self.amount = validated_data.get('amount')


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
