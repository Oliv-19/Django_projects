from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
   # path('search', views.search, name='search'),
    path('search', views.search, name='search'),
    path('biblioteca', views.biblioteca, name='biblioteca'),
    path('content/<int:pk>', views.content, name='content'),
    path('add', views.add, name='add'),
    path('addNewContent', views.addNewContent, name='addNewContent'),
    path('delete', views.delete, name='delete'),
    path('edit/<int:pk>', views.content_edit, name='content_edit'),
    path('author/<str:author_name>', views.filter_author, name='filter_author'),
    path('userRating/<int:user_id>/<int:content_id>/<int:rating>', views.userRating, name='userRating'),
    path('logout/', views.exit, name='exit'),
    path('register', views.register, name='register'),
]