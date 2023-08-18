from rest_framework import serializers
from .models import User


# создаем сериализатор для работы с данными пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'auth_code', 'invite_code', 'activated_invite_code']