from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from blog.models import Post


class HomePageView(generic.ListView):
    model = Post
    template_name = 'home_page.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_details.html'


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = '__all__'
    template_name = 'create_post.html'
    login_url = '/login/'


# class ProfileView(LoginRequiredMixin, generic.DetailView):
#     model = User
#     template_name = 'profile.html'
#     login_url = '/login/'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts_list'] = Post.objects.filter(user_id=pk)

@login_required(login_url='/login/')
def profile_view(request, pk):
    profile = User.objects.get(id=pk)
    posts = Post.objects.filter(author_id=pk)
    return render(request, "profile.html", {"profile": profile, "posts": posts})
