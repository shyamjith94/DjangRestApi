from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import (
    Tag,
    Ingredients
    )


# Create your views here.

class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Recipe Tag View Set To Manage The DataBase"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # overriding default query set function
    def get_queryset(self):
        """Return Objects Only Current Authenticated User"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create New Tag"""
        serializer.save(user=self.request.user)


class IngredientsViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    """Ingredients View Set To manage Ingredients In DataBase"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredients.objects.all()
    serializer_class = serializers.IngredientsSerializer

    # overriding default query set function
    def get_queryset(self):
        """Return Objects Only Current Authenticated User"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
