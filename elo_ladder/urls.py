from django.conf.urls import patterns, url

from elo_ladder import views

urlpatterns = patterns('',
	url(r'^$', views.standings, name='standings'),
	url(r'^report/$', views.report_results, name='report_results'),
)