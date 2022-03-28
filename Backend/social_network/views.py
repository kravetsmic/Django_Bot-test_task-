from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from .permissions import UserPostPermission

from .models import Post
from django.contrib.auth.models import User
from .serializers import UserSerializer, PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [
        TokenAuthentication,
    ]

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [
                permissions.AllowAny(),
            ]

        return [
            permissions.IsAuthenticated(),
        ]

    @action(methods=["patch"], detail=False)
    def view_post(self, request):
        user = request.user
        try:
            post = Post.objects.get(pk=request.data["post_id"])
        except Post.DoesNotExist:
            return Response(
                {"details": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if post not in user.viewed_posts.all():
            user.viewed_posts.add(post)
            return Response(
                {
                    "username": user.username,
                    "viewed_posts": self.serializer_class(user).data[
                        "viewed_posts"
                    ],
                    "success": "true",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"details": "Post is already viewed", "success": "false"},
                status.HTTP_204_NO_CONTENT,
            )

    @action(methods=["patch"], detail=False)
    def like_post(self, request):
        user = request.user
        try:
            post = Post.objects.get(pk=request.data["post_id"])
        except Post.DoesNotExist:
            return Response(
                {"details": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if post not in user.liked_posts.all():
            user.liked_posts.add(post)
            return Response(
                {
                    "username": user.username,
                    "liked_posts": self.serializer_class(user).data[
                        "liked_posts"
                    ],
                    "success": "true",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"details": "Post is already viewed", "success": "false"},
                status.HTTP_204_NO_CONTENT,
            )

    @action(methods=["patch"], detail=False)
    def dislike_post(self, request):
        user = request.user
        try:
            post = Post.objects.get(pk=request.data["post_id"])
        except Post.DoesNotExist:
            return Response(
                {"details": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if post in user.liked_posts.all():
            user.liked_posts.remove(post)
            return Response(
                {
                    "username": user.username,
                    "liked_posts": self.serializer_class(user).data[
                        "liked_posts"
                    ],
                    "success": "true",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"details": "Post is already viewed", "success": "false"},
                status.HTTP_204_NO_CONTENT,
            )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [
        TokenAuthentication,
    ]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                permissions.AllowAny(),
            ]

        return [permissions.IsAuthenticated(), UserPostPermission()]

    def create(self, request, **kwargs):
        post_data = dict(request.data)
        post_data["author"] = request.user
        serializer = self.serializer_class()
        try:
            post = serializer.create(post_data)
        except (TypeError, ValueError):
            return Response(
                {"detail": "Wrong input"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            self.serializer_class(post).data, status=status.HTTP_201_CREATED
        )
