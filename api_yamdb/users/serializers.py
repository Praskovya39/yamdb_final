import re
from rest_framework import serializers
from users.models import User
from api_yamdb.settings import (
    LEN_EMAIL, LEN_USERNAME, USERNAME_PATTERN, SELF_USERNAME
)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')


class SignUpSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Данный email занят.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Данный username занят.'
            )
        return data

    def validate_email(self, value):
        if len(value) > LEN_EMAIL:
            raise serializers.ValidationError(
                'Количество символов поля email не должно превышать '
                f'{LEN_EMAIL}')
        return value

    def validate_username(self, value):
        if re.fullmatch(USERNAME_PATTERN, value) is None:
            raise serializers.ValidationError(
                'Поле username не соответсвует паттерну')
        if len(value) > LEN_USERNAME:
            raise serializers.ValidationError(
                'Количество символов поля '
                f'username не должно превышать {LEN_USERNAME}')
        if value == SELF_USERNAME:
            raise serializers.ValidationError(
                f'Значение поля username не может быть {SELF_USERNAME}')
        return value

    class Meta:
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role'
        )


class UserNotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        read_only_fields = ('role',)
