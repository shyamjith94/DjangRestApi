from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import (
    Tag,
    Ingredients
    )


class BaseRecipeViewClass(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
    ):
    """The Class Using To Avoid Duplication Of Code"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Object That Return Current Authenticated Users Only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create New Object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeViewClass):
    """Recipe Tag View Set To Manage The DataBase"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientsViewSet(BaseRecipeViewClass):
    """Ingredients View Set To manage Ingredients In DataBase"""
    queryset = Ingredients.objects.all()
    serializer_class = serializers.IngredientsSerializer

