"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from blog.views import HomePageView

from blog.views import RegisterView, CreatePostView, PostDetailView, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>', profile_view, name='profile_page')
]
