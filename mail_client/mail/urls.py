from django.conf.urls import url

from . import views

app_name='mail'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^u/0/inbox$', views.inbox, name='inbox'),
    #Go through emails 1-20 (+ is for extra digits)
    url(r'^u/0/inbox/(?P<email_id>[0-9]+)$', views.email, name='email'),
    url(r'^ajax/receiver$', views.receiver, name='receiver'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^api$', views.assign_credentials, name='api'),
    # url(r'^next_email$', views.next_email, name='next_email'),
]
