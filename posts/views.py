from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Hashtag, Post

from django.core.paginator import Paginator

# Create your views here.
def index(request):
    posts= Post.objects.all()
    paginator = Paginator(posts, 4)

    page = request.GET.get('page')
    posts = contacts = paginator.get_page(page)

    context = {
        'posts':posts
    }
    return render(request,'posts/index.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for word in post.content.split():
                if word.startswith('#'):
                    hashtag= Hashtag.objects.get_or_create(content=word)[0] # (obj, True or False)
                    post.hashtags.add(hashtag)
            return redirect("posts:index")

    else:
        form = PostForm()
    context = {
        'form':form
    }
    return render(request, 'posts/form.html', context)

def hashtags(request, id):
    hashtag = get_object_or_404(Hashtag, id=id)
    posts = hashtag.taged_post.all()
    
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    posts = contacts = paginator.get_page(page)

    context = {
        'posts':posts
    }
    return render(request, 'posts/index.html', context)

@login_required
def like(request,id):
    post = get_object_or_404(Post,id=id)
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)

    return redirect('posts:index') 

@login_required
def post_delete(request,id):
    post =get_object_or_404(Post,id=id)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')

@login_required
def post_update(request,id):
    post= get_object_or_404(Post, id=id)
    if request.user == post.user:
        if request.method == "POST":
            form =PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                post.hashtags.clear()
                for word in post.content.split():
                    if word.startswith('#'):
                        hashtag= Hashtag.objects.get_or_create(content=word)[0] # (obj, True or False)
                        post.hashtags.add(hashtag)
            
                return redirect('posts:index')
        else:
            form =PostForm(instance=post)
        context={
            'form':form
        }
        return render(request,'posts/form.html', context)
    return redirect('posts:index')
