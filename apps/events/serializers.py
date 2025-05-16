from rest_framework import serializers
from .models import Event


class EventListCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Event
        fields = (
            "title",
            "slug",
            "description",
            "date",
            "start_time",
            "end_time",
            "location",
            "max_participants",
            "image",
        )


class EventRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "slug",
            "description",
            "date",
            "start_time",
            "end_time",
            "location",
            "max_participants",
            "image",
        )
        
        extra_kwargs = {
            "slug": {"read_only": True},
            
        }
