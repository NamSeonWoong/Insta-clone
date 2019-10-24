from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('hashtags/<int:id>/', views.hashtags, name="hashtags"),
    
    path('<int:id>/post_delete/', views.post_delete, name="post_delete"),
    path('<int:id>/post_update', views.post_update, name="post_update"),
    
    path('<int:id>/like/', views.like, name="like"),

]
