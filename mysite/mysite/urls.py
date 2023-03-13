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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog.views import HomePageView, PasswordsChangeView, PostUpdateView, RegisterView, \
    ShowProfilePageView, create_post, feedback, logout_view, password_success, post_detail, \
    posts, profile, profile_view  # noqa I100

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', HomePageView.as_view(), name='home'),
    path('post/<int:pk>', post_detail, name='post_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('create/', create_post, name='create_post'),
    path('profile/<int:pk>', profile_view, name='profile_page'),
    path('loguot/', logout_view, name='logout'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update_post'),
    path('edit-profile/<int:pk>', profile, name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('password-success', password_success, name='password_success'),
    path('user-profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile_page'),

    path('feedback/', feedback, name='feedback'),
    path('posts/<int:pk>', posts, name='posts')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
