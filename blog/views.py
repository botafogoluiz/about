from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    return render(request, "blog/post_detail.html", {"post": post})
