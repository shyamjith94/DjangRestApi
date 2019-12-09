from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (
    get_user_model,
    authenticate
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer For The user Object"""

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'name'
            )
        extra_kwargs = {
            'password': {
                'write_only': True, 'min_length': 8
                }
            }

    def create(self, validated_data):
        """Create New with Encrypted Password And Return It"""
        return get_user_model().object.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer For User Authentication Object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={
            'input_type': 'password'
            },
        trim_whitespace=False
        )

    def validate(self, attrs):
        """Validate And Authenticate User"""
        email = attrs.get('email', '')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
            )
        if not user:
            msg = _('Unable To Authenticate With Provided Credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
