from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import random
import time


@api_view(['POST'])
def send_auth_code(request):
    phone_number = request.data['phone_number']
    user = User.objects.filter(phone_number=phone_number).first()

    if not user:
        # Если пользователь не найден, создаем новую запись
        user = User.objects.create(phone_number=phone_number)
    else:
        # Если пользователь существует, генерируем новый код авторизации
        user.auth_code = random.randint(1000, 9999)
        user.save()

    # Имитация задержки на сервере
    time.sleep(2)

    return Response({'auth_code': user.auth_code})


@api_view(['POST'])
def verify_auth_code(request):
    phone_number = request.data['phone_number']
    auth_code = request.data['auth_code']
    user = get_object_or_404(User, phone_number=phone_number, auth_code=auth_code)

    # Сбрасываем код авторизации после успешной проверки
    user.auth_code = None
    user.save()

    return Response({'message': 'Авторизация выполнена успешно'})


@api_view(['POST'])
def update_invite_code(request):
    phone_number = request.data['phone_number']
    invite_code = request.data['invite_code']
    user = get_object_or_404(User, phone_number=phone_number)

    # При первой авторизации генерируем и присваиваем инвайт-код
    if not user.invite_code:
        user.invite_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
    else:
        # Если пользователь уже активировал инвайт-код, выводим его
        user.activated_invite_code = user.invite_code

    # Проверяем существование чужого инвайт-кода и обновляем его
    if User.objects.filter(invite_code=invite_code).exists():
        user.invite_code = invite_code

    user.save()

    return Response({'message': 'Инвайт-код обновлен'})


@api_view(['GET'])
def profile(request):
    phone_number = request.query_params.get('phone_number')
    user = get_object_or_404(User, phone_number=phone_number)

    # Получаем список пользователей, введших инвайт-код текущего пользователя
    invited_users = User.objects.filter(invite_code=user.invite_code).values_list('phone_number', flat=True)

    return Response({'phone_number': user.phone_number, 'invite_code': user.invite_code, 'invited_users': invited_users})
