from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework_simplejwt.tokens import RefreshToken

from SpriterReact.models import SpUser, Post, PostLike
from SpriterReact.serializers import UserSerializer, CheckLoginSerializer, LoginSerializer, PostSerializer, \
    PostCreateSerializer, PostGetSerializer


# Create your views here.
class SignUpView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({"refresh" : str(refresh), "access" : str(refresh.access_token),}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CheckLoginRegisteredView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CheckLoginSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data['login']
            is_registered = SpUser.objects.filter(login=login).exists()
            return Response({"exists": is_registered}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': str(user.id)
            })
        return Response(serializer.errors, status=400)

class PostListView(generics.ListAPIView): # для отображения ленты
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateView(generics.CreateAPIView): # для создания поста
    serializer_class = PostCreateSerializer

class PostGetView(generics.ListAPIView):
    def get(self, request, post_id):
        post = Post.objects.filter(post_id=post_id).first()
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostGetSerializer(post)
        return Response(serializer.data)


class PostLikeView(generics.GenericAPIView):
    serializer_class = PostSerializer

    def post(self, request, id):
        post = Post.objects.get(post_id=id)
        user_id = request.data.get('user_id')

        liked = PostLike.objects.filter(post=post, user_id=user_id).exists()

        if liked:
            # Если пользователь уже поставил лайк, уменьшаем количество лайков
            if post.likes_count > 0:
                post.likes_count -= 1
                post.save()

            PostLike.objects.filter(post=post, user_id=user_id).delete()
            liked = False
        else:
            # Если пользователь не ставил лайк, увеличиваем количество лайков
            post.likes_count += 1
            post.save()

            # Создаем запись о лайке
            post_like = PostLike(post=post, user_id=user_id)
            post_like.save()

            liked = True

        # Обновляем состояние liked в сериализаторе
        serializer = self.get_serializer(post)
        data = serializer.data
        data['liked'] = liked

        return Response(data, status=status.HTTP_200_OK)