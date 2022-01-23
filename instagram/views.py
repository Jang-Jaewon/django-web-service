from django.shortcuts import render

from .models          import Post

def post_list(request):
    qs      = Post.objects.all()
    keyword = request.GET.get('keyword', '')
    if keyword:
        qs = qs.filter(message__icontains=keyword)
    return render(request, 'instagram/post_list.html', {'post_list':qs, 'keyword':keyword})
