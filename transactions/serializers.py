from rest_framework import serializers


from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'performed_on']

    def create(self, validated_data):
        account = validated_data.get('performed_on')
        performed_by = self.context.get('request').user
        type = validated_data.get('type')
        amount = validated_data.get('amount')

        if validated_data.get('type') == 'TOP_UP':
            account.balance += amount
            account.save()

        Transaction.objects.create(type=type,
                                    amount=amount,
                                    performed_on=account,
                                    performed_by=performed_by)
        return validated_data
