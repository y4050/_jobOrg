from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('accounts/signup', views.signup, name='signup'),
    path('jobs/', views.jobs_index, name='jobs'),
    path('jobs/<int:job_id>/', views.jobs_show, name='jobs_show'),
    path('jobs/cat/<int:cat_id>/', views.jobs_show_cat, name='jobs_show_cat'),
    path('jobs/save/<int:job_id>/', views.save_job, name='save_job'),
    path('jobs/save/cat/<int:job_id>/', views.save_cat, name='save_cat'),
    path('jobs/detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/detail/des/<int:job_id>/', views.job_description, name='job_description'),
    path('jobs/detail/de/<int:job_id>/', views.saved_job_description, name='saved_job_description'),
    path('jobs/saved/', views.jobs_saved, name='jobs_saved'),
    path('jobs/savedcats/', views.cats_saved, name='cats_saved'),
    path('jobs/<int:pk>/delete/', views.JobDelete.as_view(), name='job_delete'),
    path('jobs/cat/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
    path('jobs/saved/<int:pk>/', views.selected_job, name='selected_job'),
    path('jobs/saved/<int:pk>/add_note/', views.add_note, name='add_note'),
]
