from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from blog.models import Article


class ArticlesListView(ListView):
    model = Article
    template_name = 'blog/blog_page.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_view.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'image')
    template_name = 'blog/article_create.html'
    success_url = reverse_lazy('blog:blog_page')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content', 'image')
    template_name = 'blog/article_update.html'

    def get_success_url(self):
        return reverse('blog:article_view', args=[self.kwargs.get('pk')])

