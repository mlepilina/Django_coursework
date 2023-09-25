from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Article
from management_service.models import Mailing, Message, Client
from management_service.services import get_cached_messages


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ('mailing_time', 'mailing_frequency', 'mailing_status', 'message', 'clients')
    template_name = 'management_service/mailing_form_create.html'
    success_url = reverse_lazy('management_service:all_mailing_view')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return form


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'management_service/all_mailing_view.html'
    success_url = reverse_lazy('management_service:all_mailing_view')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['mailing_count'] = Mailing.objects.count()
        context['active_mailing_count'] = Mailing.objects.filter(mailing_status='запущена'). count()

        return context


class RandomArticlesListView(ListView):
    model = Article
    template_name = 'management_service/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles_count'] = Article.objects.count()
        context['clients_count'] = Client.objects.count()
        context['mailing_count'] = Mailing.objects.count()
        context['active_mailing_count'] = Mailing.objects.filter(mailing_status='запущена').count()

        return context


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'management_service/one_mailing_view.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404('Нет прав для действия')
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['message'] = get_cached_messages(self.object.pk)

        return context_data


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('mailing_time', 'mailing_frequency', 'mailing_status', 'message', 'clients')
    template_name = 'management_service/mailing_form_create.html'

    def get_success_url(self):
        return reverse('management_service:one_mailing_view', args=[self.kwargs.get('pk')])


class ChangeMailingStatus(UpdateView):
    model = Mailing
    fields = ('mailing_status',)
    template_name = 'management_service/change_mailing_status.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_staff:
            raise Http404('Нет прав для действия')
        return self.object

    def get_success_url(self):
        return reverse('management_service:one_mailing_view', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'management_service/mailing_delete.html'
    success_url = reverse_lazy('management_service:all_mailing_view')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404('Нет прав для действия')
        return self.object


class MessageCreateView(CreateView):
    model = Message
    fields = ('message_subject', 'message_text',)
    template_name = 'management_service/mailing_form_create.html'
    success_url = reverse_lazy('management_service:mailing_create')


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'surname', 'name', 'patronymic', 'comment',)
    template_name = 'management_service/client_create.html'
    success_url = reverse_lazy('management_service:extra_page')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    template_name = 'management_service/all_clients_view.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404('Нет прав для действия')
        elif self.request.user.has_perm:
            return self.object
        return self.object


class ClientDetailView(DetailView):
    model = Client
    template_name = 'management_service/one_client_view.html'


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'surname', 'patronymic', 'email', 'comment')
    template_name = 'management_service/client_create.html'
    success_url = reverse_lazy('management_service:all_clients_view')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'management_service/client_delete.html'
    success_url = reverse_lazy('management_service:all_clients_view')





