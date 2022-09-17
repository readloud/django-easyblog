from django.contrib import admin
from django.urls import path
from .views import *
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('blogs/', BlogListView, name='blogs'),
    path('blog/<int:_id>', BlogDetailView, name='blog'),
]