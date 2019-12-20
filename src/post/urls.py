from django.urls import path

from .views import PostListView, PostDetailView, SearchPostResultView, \
                   PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<uuid:pk>', PostDetailView.as_view(), name='post_detail'),
    path('create', PostCreateView.as_view(), name='post_create'),
    path('<uuid:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<uuid:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('search', SearchPostResultView.as_view(), name='search_results')
]
