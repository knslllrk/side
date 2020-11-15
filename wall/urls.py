from django.urls import path
from . import views


app_name = 'wall'
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('', views.PostList.as_view(), name='post'),
    path('<int:pk>', views.detail, name='detail'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/edit', views.edit, name='edit'),
    path('new', views.post_new, name='post_new'),
    path('<int:pk>/like/', views.like, name='like'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.Search.as_view(), name='search'),
]