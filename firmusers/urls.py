from django.urls import path
from . import views
from .views import *
from .views import ProjectListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('', views.index, name='index'),
  path("logout/", views.logout_user, name='logout'),
  path("register/", views.register_user, name='register'),
  path('<int:id>', views.view_firmuser, name='view_firmuser'),
  path('add/', views.add, name='add'),
  path('projects/', ProjectListView.as_view(), name='projects'),
  path('delete_project/<int:id>/', views.delete_project, name='delete_project'),
  path('edit_project/<int:id>/', views.edit_project, name='edit_project'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('archive/', ArchiveListView.as_view(), name='archive'),

  path('profile/<int:id>/', profile, name='profile'),
  
  path('tasks/', views.tasks, name='tasks'),
  path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
  path('edit_task/<int:id>/', views.edit_task_with_subtasks, name='edit_task'),
  
  path('podryad/', PodryadListView.as_view(), name='podryad'),
  path('delete_podryad/<int:id>/', views.delete_podryad, name='delete_podryad'),
  path('edit_podryad/<int:id>/', views.edit_podryad, name='edit_podryad'),

  path('project_open/<int:id>/', views.project_open, name='project_open'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)