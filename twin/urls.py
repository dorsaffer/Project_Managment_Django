from django.conf.urls import url
from django.urls import re_path, path
from django.contrib.auth.views import LoginView
from twin import views

urlpatterns = [
    #path('inscri/', views.register_user, name='inscri'),
    #path('login/', views.login_user, name="login"),
    #path('logout/', views.logout_user, name="logout"),
    path('test/',views.test,name="test"),
    re_path(r'^$', views.index, name='index'),
    path('projects/', views.projects, name='liste'),
    path('projects/<int:pId>/', views.project_details, name='details'),
    path('projects_liste/',views.list_projects,name='projet_liste' ),
    #re_path(r'^projects/(?P<pId>[0-9]+)/edit/$', views.edit_project, name='edit')
    path('projects/<int:pId>/edit/', views.edit_project, name='edit'),
    path('projects/create/', views.add_project, name='create'),
    path('post/',views.index_post,name='post'),
    path('show/<int:id>/',views.show_post,name='show'),
    path('delete/<int:id>/',views.Delete_project,name='delete'),
    path('search-form/', views.search_form),
    url('search/', views.search),




]