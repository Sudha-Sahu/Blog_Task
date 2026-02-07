from django.shortcuts import render
from .models import Post

def blog_home(request):
    posts = Post.objects.all()
    return render(request, 'blog_home.html', {'posts': posts})
