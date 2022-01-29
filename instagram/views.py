from django.contrib                 import messages
from django.shortcuts               import get_object_or_404, render, redirect
from django.views.generic           import ListView, DetailView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.contrib.auth.mixins     import LoginRequiredMixin

from .models import Post
from .forms  import PostForm


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '포스팅을 저장했습니다.')
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html', {'form': form, 'post': None,})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, '작성자만 수정할 수 있습니다.')
        return redirect(post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, '포스팅을 수정했습니다.')
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(request, 'instagram/post_form.html', {'form': form, 'post': post,})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '포스팅을 삭제했습니다.')
        return redirect('instagram:post_list')
    return render(request, 'instagram/post_confirm_delete.html', {'post': post,})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
post_list = PostListView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs

post_detail = PostDetailView.as_view()


post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)


post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)
