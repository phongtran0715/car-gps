from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext as _


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
        message="email message phongtran0715")])
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password", "date_joined")

    def validate_password(self, password):
        data = self.get_initial()
        if password != data['confirm_password']:
            raise serializers.ValidationError(_("Those passwords don't match."))
        return password

    def validate(self, attrs):
        del attrs['confirm_password']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': "User account is disabled.",
        'invalid_credentials': "Unable to login with provided credentials."
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(_(self.error_messages['inactive_account']))
            return attrs
        else:
            raise serializers.ValidationError(_(self.error_messages['invalid_credentials']))


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    refresh = serializers.CharField()

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(_('Current password does not match'))
        return value

    # def validate_new_password(self, value):
    #     password_validation.validate_password(value)
    #     return value


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
