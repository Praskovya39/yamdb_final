from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets, pagination, permissions, filters, status

from api_yamdb.settings import SELF_USERNAME
from users.models import User
from users.serializers import (
    TokenSerializer, SignUpSerializers, UserSerializer)
from users.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    pagination_class = pagination.LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        url_path=SELF_USERNAME,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_self(self, request):
        instance = request.user
        if request.method != 'PATCH':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        serializer = self.get_serializer(
            instance,
            request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=instance.role, partial=True)
        return Response(serializer.data)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            data = {
                'username': serializer.validated_data['username'],
                'token': str(token)
            }
            return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email']
    )
    confirmation_code = default_token_generator.make_token(user)
    user.email_user(
        subject='Ваш код',
        message=f'Код подтверждения - {confirmation_code}',
        from_email=settings.EMAIL_YAMDB
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
