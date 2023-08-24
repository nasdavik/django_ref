from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
import random
import time


@api_view(['POST'])
def send_auth_code(request):
    phone_number = request.data['phone_number']
    user = User.objects.filter(phone_number=phone_number).first()

    if not user:
        # Если пользователь не найден, создаем новую запись
        user = User.objects.create(phone_number=phone_number)

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

    # При первой авторизации генерируем и присваиваем инвайт-код
    if not user.invite_code:
        user.invite_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))

    # Сбрасываем код авторизации после успешной проверки
    user.auth_code = None
    user.save()

    return Response({'message': 'Авторизация выполнена успешно', 'invate_code': f'{user.invite_code}'})


@api_view(['POST'])
def update_invite_code(request):
    phone_number = request.data['phone_number']
    invite_code = request.data['invite_code']
    user = get_object_or_404(User, phone_number=phone_number)

    if user.activated_invite_code:
        return Response({'message': f'Ваш инвайт-код: {user.activated_invite_code}'})

    # Проверяем существование чужого инвайт-кода и обновляем его
    elif User.objects.filter(invite_code=invite_code).exists():
        user.activated_invite_code = user.invite_code
        user.save()
        return Response({'message': 'Инвайт-код обновлен'})

    else:
        return Response({'message': 'Такого инвайт-кода не существует. Проверьте, правильно ли вы его написали '})


@api_view(['GET'])
def profile(request):
    phone_number = request.query_params.get('phone_number')
    user = get_object_or_404(User, phone_number=phone_number)

    # Получаем список пользователей, введших инвайт-код текущего пользователя
    invited_users = User.objects.filter(invite_code=user.invite_code).values_list('phone_number', flat=True)

    return Response({'phone_number': user.phone_number, 'invite_code': user.invite_code, 'invited_users': invited_users})
