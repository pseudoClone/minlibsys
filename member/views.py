from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import MemberSignUpSerializer
from rest_framework import generics


class MemberRegistrationView(generics.CreateAPIView):
    serializer_class = MemberSignUpSerializer
    permission_classes = [AllowAny]
