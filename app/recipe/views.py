from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import Tag


# Create your views here.

class TagViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
        ):
    """Recipe Tag View Set To Manage The DataBase"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # overriding default query set function
    def get_queryset(self):
        """Return Objects Only Current Authenticated User"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
