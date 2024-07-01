from django.contrib.auth import authenticate
from rest_framework import serializers

from SpriterReact.models import SpUser, Post, PostLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpUser
        fields = ['login', 'password', 'first_name', 'last_name', 'middle_name', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}  # Указываем, что поле пароля не должно быть доступно для чтения
        }

    def create(self, validated_data):
        return SpUser.objects.create_user(**validated_data)


class CheckLoginSerializer(serializers.Serializer):
    login = serializers.EmailField()

    def validate_login(self, value):
        return value


class LoginSerializer(serializers.Serializer):
    login = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')
        user = authenticate(login=login, password=password)
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Unable to log in with provided credentials.")

class UserFIOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpUser
        fields = ["last_name", "middle_name", "first_name"]
class PostSerializer(serializers.ModelSerializer): # для возвращения в ленту всех постов
    user = UserFIOSerializer()
    liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["post_id", "title", "small_text", "likes_count", "user", "liked"]

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем, лайкнул ли пользователь пост
            user = request.user
            liked = PostLike.objects.filter(post=obj, user=user).exists()
            return liked
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "small_text", "full_text", "image_src", "user"]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

class PostGetSerializer(serializers.ModelSerializer): # для получения определенного поста при клике из ленты
    user = UserFIOSerializer()
    class Meta:
        model = Post
        fields = '__all__'