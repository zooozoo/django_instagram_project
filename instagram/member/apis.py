from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, SignupSerializer

User = get_user_model()


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(
            username=username,
            password=password,
        )
        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': 'Invalid credentials'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # username = request.data['username']
        # password = request.data['password']
        #
        # if User.objects.filter(username=username).exists():
        #     return Response({'message': 'Username already exist'})
        #
        # user = User.objects.create_user(
        #     username=username,
        #     password=password,
        # )
        # token = Token.objects.create(user=user)
        # data = {
        #     'user': UserSerializer(user).data,
        #     'Token': token.key,
        # }
        # return Response(data)


class FacebookLogin(APIView):
    def post(self, request):
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            issued_at: int
            scopes: list
            type: str
            user_id: str

        def get_debug_token_info(token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            return DebugTokenInfo(**response.json()['data'])

        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        user = authenticate(facebook_user_id=request.data['facebook_user_id'])

        if not user:
            user = User.objects.create_user(
                username=f'fb{request.data["facebook_user_id"]}',
                user_type=User.USER_TYPE_FACEBOOK,
                age=request.data['age']
            )
        data = {
            'user': UserSerializer(user).data,
            'token': user.token,
        }
        return Response(data)
