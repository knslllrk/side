from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from .forms import ContactForm, PostForm, UserLoginForm, UserRegisterForm
from .models import Comment, Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Вы успешно зарегистрировались')
            form.save()
            return redirect('wall:login')
        else:
            messages.error(request, 'Ошибка регистрации')    
    else:
        form = UserRegisterForm()
    return render(request, 'wall/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('wall:post')
    else:
        form = UserLoginForm()
    return render(request, 'wall/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('wall:login')


class PostList(ListView):
    model = Post
    template_name = 'wall/index.html'
    context_object_name = 'latest_post_list'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    latest_comment_list = post.comment_set.order_by('id')[:10]
    return render(request, 'wall/detail.html', {'post': post, 'latest_comment_list': latest_comment_list})


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.comment_set.create(
        author=request.POST['name'], text_comment=request.POST['text'])
    return HttpResponseRedirect(reverse('wall:detail', args=(post.pk,)))


def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.author_name = request.user
            post.save()
            return redirect('wall:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'wall/edit.html', {'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.author_name = request.user
            post.save()
            return redirect('wall:post')
    else:
        form = PostForm()
    return render(request, 'wall/edit.html', {'form': form})


def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_tags = User.objects.filter(users_post_main=pk)
    current_user = request.user
    if current_user not in user_tags:
        try:
            post = get_object_or_404(Post, pk=pk)
            post.thumbnumber += 1
            post.likedone.add(current_user)
            post.save()
            return redirect('wall:detail', pk=post.pk)
        except ObjectDoesNotExist:
            return redirect('wall:detail', pk=post.pk)
    else:
        return redirect('wall:detail', pk=post.pk)
    return render(request, 'wall/detail.html', {"post": post, "thumbnumber": thumbnumber})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], form.cleaned_data['email'], ['makandrovew@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('wall:post')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'wall/contact.html', {"form": form})


class Search(ListView):
    template_name = 'wall/search.html'
    context_object_name = 'latest_post_list'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(title_text__contains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = F("s={self.request.GET.get('s')}&")
        return context
