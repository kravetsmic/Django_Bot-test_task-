from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "posts",
            "liked_posts",
            "viewed_posts",
        )
        read_only_fields = ("posts", "liked_posts", "viewed_posts", "author")
        extra_kwargs = {
            "password": {"required": False},
            "username": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        Token.objects.create(user=user)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        if "password" in validated_data.keys():
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("views", "likes", "author")
