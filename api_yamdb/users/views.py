from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import GetTokenSerializer, RegistrationSerializer

User = get_user_model()


class GetTokenAPIView(APIView):
    """
    Получить/обновить токен.
    """

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Предоставлен неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет)
    доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        email_info = (
            f'Здравствуйте {user.username}'
            f'\n Ваш проверочный код для завершения регистрации:'
            f'{confirmation_code}'
        )
        data = {
            'email_info': email_info,
            'to_email': user.email,
            'mail_subject': 'Код подтверждения для регистрации на сайте YaMDB'
        }
        self.__send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def __send_email(data):
        email = EmailMessage(
            subject=data['mail_subject'],
            body=data['email_info'],
            to=[data['to_email']]
        )
        email.send()
