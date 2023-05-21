from django.urls import path
from . import views

app_name='core'

urlpatterns = [
    path('',views.index, name='index'),
    path('settings/',views.settings, name='settings'),
    # upload does not upload/
    path('upload',views.upload, name='upload'),
    path('follow',views.follow, name='follow'),
    path('search',views.search, name='srearch'),
    # path('profile/<str:pk>',views.profile, name='profile'),
    path('like-post',views.like_post, name='like-post'),
    

]
