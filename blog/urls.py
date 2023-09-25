from django.urls import path

from blog.views import ArticlesListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

app_name = 'blog'

urlpatterns = [
    path('blog_page', ArticlesListView.as_view(), name='blog_page'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('update/<int:pk>/', ArticleUpdateView.as_view(), name='update'),
    path('article_view/<int:pk>/', ArticleDetailView.as_view(), name='article_view'),
]

