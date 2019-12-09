from user.serializer import UserSerializer
from rest_framework import generics


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """Create New User In The System"""
    serializer_class = UserSerializer

