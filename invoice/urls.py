from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home_page, name='home_page'),
	url(r'^resident-list/$', views.household_list, name ="household_list"),
	url(r'^upload-spreadsheet/$', views.display_form, name ="display_form"),
	url(r'^upload-spreadsheet/success_upload/$', views.success_upload, name ="success_upload"),
	url(r'^invoices/$', views.invoices, name = 'invoices'),
	url(r'^send-invoice/$', views.send_invoice, name = 'send_invoice'),
	url(r'^edit-invoice/(?P<pk>\d+)/$', views.edit_invoice, name='edit_invoice'),
	url(r'^edit-household/(?P<pk>\d+)/$', views.edit_household, name='edit_household'),
	url(r'^sale-list/$', views.sale_list, name='sale_list'),
	url(r'^sale-list/$', views.sale_list, name='sale_list'),
	url(r'^agent-form/(?P<pk>\d+)/$', views.agent_form, name='agent_form'),
	url(r'^agent-confirmation/$', views.agent_thank_you, name='agent_thank_you'),
]