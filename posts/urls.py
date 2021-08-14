from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', ListAPIView, name='home'), # Lists all the posts & Add posts
    path('posts/<int:pk>/', DetailAPIView, name='post'),
    path('posts/delete/<int:pk>/', PostDeleteAPIView, name='post_delete'),
    path('posts/<int:post_id>/vote/<int:vote_type>/', PostVoteAddAPIView, name='add_post_vote'),
    path('posts/<int:pk>/comments/', CommentAddAPIView, name='add_comment'),
    path('posts/<int:pk>/comments/<int:comment_id>/reply/', CommentReplyAPIView, name='reply_comment'),
    path('posts/search/<tag_name>/', TagSearchAPIView, name='search_tags'),   
]