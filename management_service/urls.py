from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from blog.views import ArticleDetailView
from management_service.apps import ManagementServiceConfig
from management_service.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MessageCreateView, ClientCreateView, RandomArticlesListView, MailingDeleteView, ClientListView, ClientDetailView, \
    ClientUpdateView, ClientDeleteView, ChangeMailingStatus

app_name = ManagementServiceConfig.name


urlpatterns = [
    path('', RandomArticlesListView.as_view(), name='home'),
    path('extra_page/', TemplateView.as_view(template_name="management_service/extra_page.html"), name='extra_page'),

    path('all_mailing_view', MailingListView.as_view(), name='all_mailing_view'),
    path('one_mailing_view/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='one_mailing_view'),
    path('mailing_form_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('change_mailing_status/<int:pk>/', ChangeMailingStatus.as_view(), name='change_mailing_status'),

    path('article_view/<int:pk>/', ArticleDetailView.as_view(), name='article_view'),

    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('all_clients_view', ClientListView.as_view(), name='all_clients_view'),
    path('one_client_view/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='one_client_view'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
