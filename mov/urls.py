from django.urls import path, reverse_lazy
from . import views
# from . import models
# from mkt.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

app_name='mov'
urlpatterns = [
    path('', views.MovieListView.as_view(), name='all'),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create',
        views.MovieCreateView.as_view(success_url=reverse_lazy('mov:all')), name='movie_create'),
    path('movie/<int:pk>/update',
        views.MovieUpdateView.as_view(success_url=reverse_lazy('mov:all')), name='movie_update'),
    path('movie/<int:pk>/delete',
        views.MovieDeleteView.as_view(success_url=reverse_lazy('mov:all')), name='movie_delete'),
    path('movie_picture/<int:pk>', views.stream_file, name='movie_picture'),
    path('movie/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='movie_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('mov:all')), name='movie_comment_delete'),
    path('movie/<int:pk>/toggle',
        views.ToggleFavoriteView.as_view(), name='movie_toggle'),
    path('search/',
        views.PostListView.as_view(), name='search'),
]