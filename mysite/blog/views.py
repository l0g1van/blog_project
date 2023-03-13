from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .models import Post, Profile

from .form import CommentForm, EditProfileForm, FeedbackForm, PasswordChangingForm,\
    PostForm, ProfileUpdateForm, RegisterForm  # noqa I100
from .task import send_feedback_email


class HomePageView(generic.ListView):
    model = Post
    template_name = 'home_page.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.order_by('-date_published')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_details.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'
    success_url = reverse_lazy('home')


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


@login_required(login_url='/login/')
def profile(request, pk):
    if request.method == 'POST':
        u_form = EditProfileForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile_page', pk=request.user.pk)
    else:
        u_form = EditProfileForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'edit_profile.html', context)


class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/password_success.html', {})


def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback-text')
        send_feedback_email.delay(feedback_text, request.user.email)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comment_list = post.comments().filter(is_published=True)
    p = Paginator(comment_list, 3)
    page = request.GET.get('page')
    comments_p = p.get_page(page)

    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user.username
            else:
                instance.user = 'anonymous'
            instance.post = post
            instance.save()
            return redirect('post_detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form,
        'comments_p': comments_p
    }
    return render(request, 'post_details.html', context)


class ShowProfilePageView(generic.DetailView):
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context


@login_required(login_url='/login/')
def posts(request, pk):
    post_list = Post.objects.filter(author__id=pk)
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts.html', {'page_obj': page_obj})


@login_required(login_url='/login/')
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    context = {
        'post': post
    }
    return render(request, 'post_delete.html', context)
