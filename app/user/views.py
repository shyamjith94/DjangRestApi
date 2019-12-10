from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import (
    generics,
    authentication,
    permissions)
from user.serializer import (
    UserSerializer,
    AuthTokenSerializer
    )


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """Create New User In The System"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create New Auth Token For User"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UpdateUserProfile(generics.RetrieveUpdateAPIView):
    """Manage Authenticate User Profile"""
    serializer_class = UserSerializer
    # "()" is needed else get Exception **
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrieve and Return Authenticated User"""
        return self.request.user
