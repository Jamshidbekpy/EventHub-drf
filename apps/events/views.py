from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Event
from .serializers import EventListCreateSerializer  

# Create your views here.

class EventListCreateAPIView(ListCreateAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListCreateSerializer
    
    
class EventRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventListCreateSerializer
    
    lookup_url_kwarg = 'slug'
    
    
class RegisterEventAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = EventListCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
