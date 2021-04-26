from django.contrib.messages import views
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, SignUpView, password_reset_request
from . import views

urlpatterns = [
  path('password/password_reset', views.password_reset_request, name='password_reset'),
  path('post/comment/', views.comment_detail, name='comment'),
  path('post/logout/', views.logout_request, name='logout'),
  path('post/login/', views.login_request, name='login'),
  path('post/register/', SignUpView.as_view(), name='register'),
  path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
  path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
  path('post/new/', BlogCreateView.as_view(), name='post_new'),
  path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
  path('', BlogListView.as_view(), name='home')
]