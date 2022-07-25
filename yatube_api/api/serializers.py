from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


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
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset = User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
    
    validators = [
        UniqueTogetherValidator(
            message='Данная подписка уже существует',
            queryset=Follow.objects.all(),
            fields=['user', 'following']
        )
    ]

    def validate_following(self, following):
        if self.context['request'].user == following:
            raise serializers.ValidationError('На себя нельзя подписываться')
        return following
