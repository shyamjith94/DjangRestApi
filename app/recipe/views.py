from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import (
    Tag,
    Ingredients,
    Recipe
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


class RecipesViewSet(viewsets.ModelViewSet):
    """Recipes View Set To Manage Recipe In Data Base"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Private Function that Convert list Of string ids to list of integer ids"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve The Recipes To Authenticated User"""
        # filter by tag, if tag is provided in query prams then it filter else its set None
        tags = self.request.query_params.get('tag')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # tag_id__id__in double underscore using for foreign key filter
            queryset = queryset.filter(tag__id__in=tag_ids)

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """For Details View Choose Serializer Class Based On User Request"""
        # for recipe detail view check request action
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        # for image field get request
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create Recipe For Authenticated User"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    # adding custom action for image upload
    def upload_image(self, request, pk=None):
        """Upload Image To Recipe Model"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.eror, status.HTTP_400_BAD_REQUEST)
