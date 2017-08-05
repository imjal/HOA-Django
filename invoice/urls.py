from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.household_list, name='household_list'),
]