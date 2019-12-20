from django.views.generic import ListView, DetailView, CreateView, \
                                 UpdateView, DeleteView

from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q


from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)


from django.http import HttpResponseRedirect

from .models import Post
from .forms import PostForm


class PostListView(ListView):

    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'post_list'
    login_url = 'login'
    paginate_by = 3


class PostDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    login_url = 'login'
    permission_required = 'post.can_open'


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'account_login'
    permission_required = ('post.can_open', 'polls.can_edit')

    def get(self, request, *args, **kwargs):
        context = {'form': PostForm()}
        return render(request, 'posts/post_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse_lazy('post_detail', args=[str(post.id)]))

        context = {'form': form}
        return render(request,  'posts/post_create.html', context)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    login_url = 'account_login'
    permission_required = ('polls.can_edit')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    login_url = 'account_login'
    permission_required = 'polls.can_delete'


class SearchPostResultView(ListView):

    model = Post
    template = 'posts/search_result.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('q')

        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(author__icontains=query))







