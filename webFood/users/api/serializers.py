from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import UserProfile, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'photo', 'gender', 'phone']


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            phone=profile_data['phone'],
            address=profile_data['address'],
            gender=profile_data['gender']
        )
        return user


class UserSigninSerializer(TokenObtainSerializer):

    def __init__(self, *args, **kwargs):
        if 'email' in kwargs['data']:
            self.username_field = 'email'
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
