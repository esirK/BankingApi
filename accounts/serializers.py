from django.contrib.auth import get_user_model
from rest_framework import serializers


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
        User.objects.create_customer(**validated_data)
        return validated_data

    def to_representation(self, instance):
        instance.pop('password')
        return instance
