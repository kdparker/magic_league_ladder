from django.conf.urls import patterns, url

from elo_ladder import views

urlpatterns = patterns('',
	url(r'^$', views.standings, name='standings'),
	url(r'^report/$', views.report, name='report'),
	url(r'^report/make/$', views.make_report, name='make_report'),
	url(r'^history/$', views.history, name='history'),
	url(r'^players/(?P<player_id>\d+)/$', views.player_details, name='player_details'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login/$', views.user_login, name='login'),
  url(r'^logout/$', views.user_logout, name='logout')
)