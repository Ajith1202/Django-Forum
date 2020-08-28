from django.urls import path
from .views import *

urlpatterns = [
    path('', ListAPIView, name='home'),
    path('posts/<int:pk>/', DetailAPIView, name='post'),
    path('posts/<int:pk>/comments/', CommentAddAPIView, name='add_comment')
]