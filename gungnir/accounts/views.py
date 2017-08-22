from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in

from dataCollector.models import Topics_model

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    UserDetailSerializer,
)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = self.queryset.get(username=serializer.data['username'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user_obj_s = UserDetailSerializer(user).data
        return Response({'token': token, 'user_data': user_obj_s}, status=HTTP_201_CREATED)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = self.queryset.get(username=serializer.data['username'])
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            print(token)
            login(request, user)
            new_data = serializer.data
            # user_obj = User.objects.filter(username=new_data['username']).first()
            user_obj_s = UserDetailSerializer(user).data
            return Response({'token':token,'user_data':user_obj_s}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(UserDetailSerializer(request.user).data, status=HTTP_200_OK)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


