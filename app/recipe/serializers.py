from rest_framework import serializers
from core.models import (
    Tag,
    Ingredients,
    Recipe
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


class RecipeSerializers(serializers.ModelSerializer):
    """Serializer For Recipe Model And Objects"""
    # ingredients and tag are not recipe model its primary key Fields so
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredients.objects.all()
        )
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
        )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'time_minute',
            'price',
            'link',
            'ingredients',
            'tag'
            )
        read_only_fields = (
            'id',
            )


class RecipeDetailSerializer(RecipeSerializers):
    """Serializer For Recipe Detail View """
    ingredients = IngredientsSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer For Upload Image"""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image'
            )
        read_only_fields = ('id',)
