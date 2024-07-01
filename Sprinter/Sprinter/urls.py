"""
URL configuration for Sprinter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from SpriterReact.views import SignUpView, CheckLoginRegisteredView, LoginView, PostListView, PostCreateView, \
    PostGetView, PostLikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/signup/', SignUpView.as_view(), name = "signup"),
    path('api/v1/check-login/', CheckLoginRegisteredView.as_view(), name = "check-login"),
    path('api/v1/newsData/', PostListView.as_view(), name='news-data'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/post-create/', PostCreateView.as_view(), name='create-post'),
    path('api/v1/posts/<uuid:post_id>/', PostGetView.as_view(), name='post-get'),
    path('api/posts/<uuid:id>/like/', PostLikeView.as_view(), name='post-like'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
