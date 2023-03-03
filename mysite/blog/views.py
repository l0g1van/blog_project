from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from blog.models import Post

from blog.form import PostForm

from blog.form import RegisterForm


class HomePageView(generic.ListView):
    model = Post
    template_name = 'home_page.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_details.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title', 'text']


# class CreatePostView(LoginRequiredMixin, generic.CreateView):
#     model = Post
#     # fields = '__all__'
#     form_class = PostForm
#     template_name = 'create_post.html'
#     login_url = '/login/'


@login_required(login_url='/login/')
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required(login_url='/login/')
def profile_view(request, pk):
    profile = User.objects.get(id=pk)
    posts = Post.objects.filter(author_id=pk)
    return render(request, "profile.html", {"profile": profile, "posts": posts})


def logout_view(request):
    logout(request)
    return redirect('home')