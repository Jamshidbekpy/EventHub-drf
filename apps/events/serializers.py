from rest_framework import serializers
from .models import Event


class EventListCreateSerializer(serializers.ModelSerializer):

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
