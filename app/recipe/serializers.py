from rest_framework import serializers
from core.models import (
    Tag,
    Ingredients
    )


class TagSerializer(serializers.ModelSerializer):
    """Serializer For Tag Objects"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name'
            )
        read_ony_fields = ('id',)


class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer For Ingredients Model And Objects"""

    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name'
            )
        red_only_fields = (
            'id',
            )

