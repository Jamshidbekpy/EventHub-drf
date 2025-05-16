from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "password_confirm")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        data = validated_data
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user
