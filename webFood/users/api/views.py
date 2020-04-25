from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.authtoken.models import Token
from users.api.serializers import UserRegistrationSerializer, UserSigninSerializer
from utils import ErrorJsonRender


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
        raise ErrorJsonRender.BadRequestException


class UserSigninView(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = UserSigninSerializer
