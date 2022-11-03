from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    UsersListView,
    SectionListView
)
from . import views

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from .feeds import LatestPostsFeed

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('', views.post_list, name='blog-home'),
    path('post/list/', PostListView.as_view(), name='blog-home-2'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),#PostDetailView.as_view()
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('blogs/', UsersListView.as_view(), name='blogs-list'),
    path('post/<int:post_id>/share/', views.post_share, name='post-share'),
    path('post/tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('blog/feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]