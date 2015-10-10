from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.view_login, name='login'),
    url(r'^home$', views.index, name='index'),
    url(r'^problems$', views.problems, name='problems'),
    url(r'^rank$', views.rank, name='rank'),
    # create
    url(r'^createTag/$', views.createTag, name='createTag'),
    url(r'^createTagAction/$', views.createTagAction, name='createTagAction'),
    
    url(r'^createUser/$', views.createUser, name='createUser'),
    url(r'^createUserAction/$', views.createUserAction, name='createUserAction'),

    url(r'^createProblem/$', views.createProblem, name='createProblem'),
    url(r'^createProblemAction/$', views.createProblemAction, name='createProblemAction'),
    
    # submit
    # ex: /polls/5/problem
    url(r'^problem/(?P<problem_id>[0-9]+)/$', views.problem, name='problem'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
]
