from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

from accounts.models import CustomerBankAccount

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        write_only = ['password']

    def validate_confirm_password(self, value):
        data = self.get_initial()
        if data.get('password') != value:
            raise serializers.ValidationError("Passwords Don't Match")


class TellerSerializer(UserSerializer):
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        User.objects.create_teller(**validated_data)
        return validated_data

    def to_representation(self, instance):
        instance.pop('password')
        return instance


class CustomerSerializer(UserSerializer):
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_customer(**validated_data)
        account = CustomerBankAccount()
        account.owner = user
        account.save()
        return validated_data

    def to_representation(self, instance):
        instance.pop('password')
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False, allow_blank=False,
                                   help_text="Email required to login")
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('email'), password=data.get('password'))
        if user:
            return {
                'email': user.email,
                'username': user.username,
                'token': user.token
            }
        raise serializers.ValidationError({"error": "Invalid credentials Were Provided"})
