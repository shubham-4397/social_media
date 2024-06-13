from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

# local imports
from apps.accounts.messages import SUCCESS_MESSAGE
from apps.accounts.serializers import SignupSerializer, LoginSerializer

USER = get_user_model()


class SignupViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
    signup class viewset
    """
    serializer_class = SignupSerializer
    queryset = USER.objects.all()

    def create(self, request, *args, **kwargs):
        """used to create a user"""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details': SUCCESS_MESSAGE['user-created']})


class LoginViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
    Login class viewset
    """
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """used to log in the user"""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        tokens = {'refresh_token': str(refresh_token),
                  'access_token': str(refresh_token.access_token)}
        return Response({'details': tokens})
