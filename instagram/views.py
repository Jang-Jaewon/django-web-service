from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic           import ListView, DetailView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.contrib.auth.mixins     import LoginRequiredMixin

from .models          import Post


# @login_required
# def post_list(request):
#     qs      = Post.objects.all()
#     keyword = request.GET.get('keyword', '')
#     if keyword:
#         qs = qs.filter(message__icontains=keyword)
#     return render(request, 'instagram/post_list.html', {'post_list':qs, 'keyword':keyword})

# @method_decorator(login_required, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
post_list = PostListView.as_view()

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'instagram/post_detail.html', {'post':post})

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
