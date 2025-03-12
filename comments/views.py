from blog.models import Post
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm

# Create your views here.

@require_POST
def comment(request, post_pk):
    #评论与文章关联，所以先获取被评论的文章，有返回文章，没有返回404
    post = get_object_or_404(Post, pk=post_pk)
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = CommentForm(request.POST)
    # 当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)
        # 将评论与文章关联
        comment.post = post
        # 保存评论数据到数据库
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功！',extra_tags='success')
        # 重定向到文章详情页
        return redirect(post)
    # 如果表单数据不合法，渲染表单页面，并显示错误信息。
    context = {'form': form, 'post': post}
    messages.add_message(request, messages.ERROR, '评论发表失败！',extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
