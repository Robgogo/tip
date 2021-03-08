from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from api.models.user import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'url',
            'email',
            'last_login',
            'first_name',
            'last_name',
            'is_active',
            'created',
        )


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        ordering = ('id',)
        fields = ('id', 'url', 'email', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}


class RestAuthRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def save(self, request):
        user = super(RestAuthRegisterSerializer, self).save(request)
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.is_active = True
        user.save()
        return user
