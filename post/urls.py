
from. import views
from django.urls import include, path

urlpatterns = [
    path('', views.all_post, name='all-posts'),
    path('<slug:topic_slug>/', views.topic_post, name='post-topic'),
    path('<slug:topic_slug>/<slug:post_slug>/', views.post, name='post'),
]