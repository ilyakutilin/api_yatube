from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп (сообществ)."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', 'posts')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    class Meta:
        model = Follow
        fields = '__all__'
