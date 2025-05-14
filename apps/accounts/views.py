from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, RetrieveAPIView,  CreateAPIView,UpdateAPIView, DestroyAPIView

# Create your views here.

class RegisterAPIVIew(CreateAPIView):
    