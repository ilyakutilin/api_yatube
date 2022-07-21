from posts.models import Comment, Follow, Group, Post
from rest_framework import viewsets

from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр информации о группах (сообществах)."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Просмотр, создание, обновление и удаление постов (публикаций)."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_permissions(self):
        """Метод, дающий доступ к получению информацию без аутентификации.
        
        При получении информации (GET / HEAD / OPTIONS запросы)
        доступ разрешен всем пользователям, включая неаутентифицированных.
        В остальных случаях доступ определяется основным пермишеном.
        """
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр, создание, обновление и удаление комментариев к постам."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Получение id поста из эндпоинта
        post_id = self.kwargs.get("post_id")
        # Выбор только комментариев, относящихся к посту
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(id=self.kwargs.get("post_id"))
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(id=self.kwargs.get("post_id"))
        )


class FollowViewSet(viewsets.ModelViewSet):
    """Просмотр, создание, обновление и отмена подписок на авторов."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
