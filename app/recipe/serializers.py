from rest_framework import serializers
from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer For Tag Objects"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name'
            )
        read_ony_fields = ('id',)
