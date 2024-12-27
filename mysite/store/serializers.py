from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserProfile
      fields =('username', 'email', 'password', 'first_name', 'last_name')
      extra_kwargs = {'password': {'write_only': True}}

   def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

   def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),

        }

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('username', 'email', 'password', 'first_name', 'last_name')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = UserProfile.objects.create_user(**validated_data)
#         return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'image', 'website']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class FollowSerializer(serializers.ModelSerializer):
    follower = UserProfileSimpleSerializer()
    following = UserProfileSimpleSerializer()

    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Post
        fields = ['user', 'image', 'video', 'description', 'created_at']


class PostSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Post
        fields = ['user']


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    post = PostSerializer()

    class Meta:
        model = PostLike
        fields = ['user', 'post', 'like', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    post = PostSimpleSerializer()
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'parent', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = CommentLike
        fields = ['user', 'comment', 'like', 'created_at']


class StorySerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Story
        fields = ['user', 'image', 'video', 'created_at']


class SavedSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Saved
        fields = ['user']


class SaveItemSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    saved = SavedSerializer()

    class Meta:
        model = SaveItem
        fields = ['post', 'saved', 'created_date']