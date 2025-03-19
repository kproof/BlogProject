from django.shortcuts import render,get_object_or_404
from .models import Post,Category, Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView

# Create your views here.
#def index(request):
    #post_list = Post.objects.all()
    #return render(request, 'blog/index.html', context={'post_list': post_list})

#类视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


#def detail(request, pk):
    #post = get_object_or_404(Post, pk=pk)
    #post.increase_views()
    #md = markdown.Markdown(extensions=[
        #'markdown.extensions.extra',
        #'markdown.extensions.codehilite',
        #TocExtension(slugify=slugify),
    #])
    #post.body = md.convert(post.body)
    #m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #post.toc = m.group(1) if m is not None else ''
    #return render(request, 'blog/detail.html', context={'post': post})
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
#def archive(request, year, month):
    #post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    #return render(request, 'blog/index.html', context={'post_list': post_list})
class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)
#def category(request, pk):
    #cate = get_object_or_404(Category, pk=pk)
    #post_list = Post.objects.filter(category=cate)
    #return render(request, 'blog/index.html', context={'post_list': post_list})
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
#def tag(request, pk):
    #tag = get_object_or_404(Tag, pk=pk)
    #post_list = Post.objects.filter(tags=tag)
    #return render(request, 'blog/index.html', context={'post_list': post_list})

