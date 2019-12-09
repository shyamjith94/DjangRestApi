from django.contrib.auth import get_user_model
from rest_framework import serializers


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
