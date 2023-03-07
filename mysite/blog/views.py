from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from blog.models import Post

from blog.form import PostForm, RegisterForm, EditProfileForm, PasswordChangingForm, ProfileUpdateForm, FeedbackForm
from blog.task import send_feedback_email


class HomePageView(generic.ListView):
    model = Post
    template_name = 'home_page.html'
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_details.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'


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


# class UserEditView(generic.UpdateView):
#     form_class = EditProfileForm
#     second_form_class = ProfileUpdateForm
#     template_name = 'edit_profile.html'
#     success_url = 'home'
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_context_data(self, **kwargs):
#         context = super(UserEditView, self).get_context_data(**kwargs)
#         if 'form' not in context:
#             context['form'] = self.form_class(self.request.GET)
#         if 'form2' not in context:
#             context['form'] = self.second_form_class(self.request.GET)
#         return context
#
#     def get(self, request, *args, **kwargs):
#         super(UserEditView, self).get(request, *args, **kwargs)
#         form = UserChangeForm(instance=request.user)
#         form2 = ProfileUpdateForm(instance=request.user)
#         return render(request, 'edit_profile.html', {'form': form, 'form2': form2})
#
#     def post(self, request, *args, **kwargs):
#         form = UserChangeForm(request.POST or None, instance=request.user)
#         form2 = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profilemodel)
#         if form.is_valid() and form2.is_valid():
#             form.save()
#             form2.save()
#             return redirect('profile_page')


@login_required(login_url='/login/')
def profile(request):
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


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('home')


def password_success(request):
    return render(request, 'registration/password_success.html', {})


# def profile(request):
#     if request.method == 'POST':
#         e_form = EditProfileForm(request.POST or None, instance=request.user)
#         p_form = ProfileUpdateForm()


def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback-text', '')
        send_feedback_email.delay(feedback_text, request.user.email)
        data = {
            'success': True,
            'message': 'Thank you for your feedback!'
        }
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
