from django.shortcuts import render, redirect
from .models import (
    Category,
    HomeSlider,
    FAQ,
    Post,
    PostGallery,
    Comment,
    PostViewsCount,
    Like, Dislike
)
from .forms import LoginForm, RegistrationForm, CommentForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.views.generic import UpdateView


# objects
# templatetags

# action =  add_like, add_dislike
# http://127.0.0.1:8000/vote/2/add_like/
def add_vote(request, post_id, action):
    post = Post.objects.get(pk=post_id)

    # try:
    #     post.likes
    # except Exception as e:
    #     Like.objects.create(post=post)
    #
    # try:
    #     post.dislikes
    # except Exception as e:
    #     Dislike.objects.create(post=post)

    if action == 'add_like':
        if request.user in post.likes.user.all():
            post.likes.user.remove(request.user.pk)
        else:
            post.likes.user.add(request.user.pk)
            post.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in post.dislikes.user.all():
            post.dislikes.user.remove(request.user.pk)
        else:
            post.dislikes.user.add(request.user.pk)
            post.likes.user.remove(request.user.pk)
    return redirect('post_detail', pk=post_id)


def index(request):
    slides = HomeSlider.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()

    context = {
        'slides': slides,
        'faqs': faqs,
        'posts': posts,
    }
    return render(request, 'blog_app/index.html', context)


def contacts(request):
    return render(request, 'blog_app/contacts.html')


# http://127.0.0.1:8000/categories/1/
def category_posts_page(request, pk):
    print(request.environ)
    search_query = request.GET.get('q')
    sort_query = request.GET.get('sort')
    category = Category.objects.get(pk=pk)
    posts = Post.objects.filter(category=category)
    if sort_query:
        posts = posts.order_by(sort_query)

    if search_query and sort_query:
        posts = posts.filter(name__iregex=search_query).order_by(sort_query)
    elif search_query:
        posts = posts.filter(name__iregex=search_query)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog_app/category.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    photos = PostGallery.objects.filter(post=post)

    comments_pagination_query = ''

    # [(1, []), (2, []), ]
    # ?query=asd
    # 14/5=3

    comments = Comment.objects.filter(post=post)
    paginator = Paginator(comments, 5)
    comments_page_number = request.GET.get('comments_page')
    paged_qs = paginator.get_page(comments_page_number)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.post = post
            form.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key

    total_post_views = PostViewsCount.objects.filter(post=post, session_id=session_id).count()
    if total_post_views == 0 and session_id != 'None':
        post_views_obj = PostViewsCount(post=post, session_id=session_id)
        post_views_obj.save()

        post.views += 1
        post.save()

    try:
        post.likes
    except Exception as e:
        Like.objects.create(post=post)

    try:
        post.dislikes
    except Exception as e:
        Dislike.objects.create(post=post)

    total_likes = post.likes.user.all().count()
    total_dislikes = post.dislikes.user.all().count()

    context = {
        'post': post,
        'photos': photos,
        'form': form,
        'comments': comments,
        'page_query': '?comments_page=',
        'paged_qs': paged_qs,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
    }
    return render(request, 'blog_app/post.html', context)


# http://127.0.0.1:8000/login/
# http://127.0.0.1:8000/registration/


def login_view(request):
    next_query = request.GET.get('next')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,
                                password=password)
            # None, User object(1)
            if user is not None:
                login(request, user)
                if next_query:
                    return redirect(next_query)
                return redirect('index')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'blog_app/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'blog_app/registration.html', context)


def logout_view(request):
    next_query = request.GET.get('next')
    logout(request)
    if next_query:
        return redirect(next_query)
    return redirect('index')


def create_post_view(request):
    if request.method == 'POST':
        # preview
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form = Post
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            for obj in request.FILES.getlist('gallery'):
                new = PostGallery(post=form, image=obj)
                new.save()
            return redirect('post_detail', pk=form.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'blog_app/post_form.html', context)


# только авторизованные пользователи могут оставлять комментарии


# model_confirm_delete.html


def delete_article(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('index')


# DeleteView
class PostUpdate(UpdateView):
    success_url = '/'
    model = Post
    form_class = PostForm
    template_name = 'blog_app/post_form.html'


def search(request):
    query = request.GET.get('q')  # nam
    # nam in name
    posts = Post.objects.filter(name__iregex=query)
    if not query:
        posts = []
    context = {
        'posts': posts,
    }
    return render(request, 'blog_app/search_results.html', context)
