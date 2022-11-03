from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import Profile
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm


from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .models import (Post, Section)

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    tag = None

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts,
        'sections': Section.objects.all(),
        'tag': tag
    }
    return render(request, 'blog/post/list.html', context)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)#, status='published'
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                         f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                         f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'olenkakopylova@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})

def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)

    new_comment = None
    comment_form = False

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_publish')[:4]


    comments = post.comments.filter(active=True)
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = user
                new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'object': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'content'),
            ).filter(search=query)
    return render(request,'blog/main/search.html', {'form': form,
                      'query': query,
                      'results': results})

def about(request):
    return render(request, 'blog/about.html', {'title': 'О клубе Python Bytes'})

class SectionListView(ListView):
    model = Section
    context_object_name = 'sections'

class PostListView(ListView):
    model = Post
    template_name = 'blog/main/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'published'
        return context

class UsersListView(ListView):
    model = User
    template_name = 'blog/user/blog_list.html'
    context_object_name = 'users'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_create')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


