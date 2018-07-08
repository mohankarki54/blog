from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment, User, Feed, Article
from django.utils import timezone
from blog.forms import PostForm, CommentForm, FeedForm, UserCreateForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


from . import forms
import feedparser


class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post


    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    

@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
    "form":form,
    }
    return render(request, 'post_form.html', context)



class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Tech News and Blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registrations.')

    else:
        form = UserCreateForm()
    return render(request, 'sign_up.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('articles_list')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# FOr like



# For comment and to publish post

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)



@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def comment_red(request,pk):
    post =  get_object_or_404(Post, pk=pk)
    return render(request,'blog/comment_redirect.html')


def articles_list(request):
    articles = Article.objects.all()

    rows = [articles[x:x+1] for x in range(0, len(articles), 1)]

    return render(request, 'blog/articles_list.html', {'rows': rows})

@login_required
def feeds_list(request):

    feeds = Feed.objects.all()
    form = FeedForm

    context = {
        'feeds': feeds,
        'form': form,
    }

    return render(request, 'blog/feeds_list.html', context)

@login_required
def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.save()


            return redirect('feeds_list')
    else:
        form = FeedForm()

    context = {
        'form': form,
    }

    return render(request, 'blog/new_feed.html', context)
