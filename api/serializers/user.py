from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
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
            'role',
        )


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, attrs):
        email = attrs['email']
        allowed_domain = 'faculty.ie.edu'
        email_domain = email.split('@')[1]
        if email_domain != allowed_domain:
            msg = 'The email domain should be "@faculty.ie.edu" only!'
            raise serializers.ValidationError(msg)
        
        return attrs

    class Meta:
        model = User
        ordering = ('id',)
        fields = ('id', 'url', 'email', 'first_name',
                  'last_name', 'password', 'role')
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}


class RestAuthRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    role = serializers.IntegerField()

    def validate_email(self, email):
        allowed_domain = 'faculty.ie.edu'
        email_domain = email.split('@')[1]
        if email_domain != allowed_domain:
            msg = _('The email domain should be "@faculty.ie.edu" only!')
            raise serializers.ValidationError(msg)
        return email

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'role': self.validated_data.get('role', 3)
        }

    def save(self, request):
        user = super(RestAuthRegisterSerializer, self).save(request)
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.is_active = True
        user.role = self.validated_data.get('role')
        user.save()
        return user
