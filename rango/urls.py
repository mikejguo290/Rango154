from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name ='index'),
    url(r'^about/$', views.about, name ='about'),
    url(r'^food/$', views.food, name='food'),
    url(r'^products/$', views.products, name ='products'),
    url(r'^add_category/$', views.add_category, name ='add_category'),
    url(r'^category/(?P<category_name_url>\w+)/$', views.category, name ='category'),
    url(r'^register/$', views.register, name ='register' ),
    url(r'^login/$',views.user_login, name ='login'),
    url(r'^restricted/$',views.restricted, name ='restricted'),
    url(r'^logout/$', views.user_logout, name ='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^history/$', views.history, name = 'history'),
    )
 # wtf? anything between category/ and the next / is passed as category_name_url to views.category template.