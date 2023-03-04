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

from blog.views import RegisterView, PostDetailView, PostUpdateView, UserEditView, PasswordsChangeView, profile_view, logout_view, create_post, password_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('create/', create_post, name='create_post'),
    path('profile/<int:pk>', profile_view, name='profile_page'),
    path('loguot/', logout_view, name='logout'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('edit-profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(template_name='change_password.html')),
    path('password-success', password_success, name='password_success')
]
