from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Author, Category, Comment
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render


@login_required
def index(request):
    categories = Category.objects.all()
    posts = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 4)

    try:
        paginator = paginator.page(page)
    except:
        paginator = paginator.page(1)

    return render(request, 'blog/blog_home.html', {
        'categories': categories,
        'page_obj': paginator,
    })


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostByCategoryView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return Post.objects.filter(category=category).order_by('-date_posted')
    
    def get_context_data(self, *args, **kwargs):
        category = self.kwargs.get('category')
        category = category.replace('-', ' ')
        context = super(PostByCategoryView, self).get_context_data(*args, **kwargs)
        context["category"] = category.capitalize()
        return context


class RequestAuthorshipView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name', 'email', 'address', 'phone', 'field_of_study', 'blog_category', 'reason']

    def form_valid(self, form):
        messages.success(self.request, "Your request to become one of our authors have been submitted successfully. We will review it shortly. Thanks 😊")
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        comments = Comment.objects.filter(post=post).order_by('-date_commented')
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['total_likes'] = post.total_likes()
        context['comments'] = comments

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context['liked'] = liked

        return context


class CommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.instance.commenter = self.request.user
        messages.success(self.request, "You've commented")
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super(CommentView, self).get_context_data(*args, **kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['pk'])
        context['button'] = 'Comment'

        return context
    

class CommentUpdateViewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']
    
    def get_context_data(self, *args, **kwargs):
        context = super(CommentUpdateViewView, self).get_context_data(*args, **kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['button'] = 'Update'
        return context
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.commenter


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))