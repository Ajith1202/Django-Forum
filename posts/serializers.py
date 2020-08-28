from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'description', 'submitted_on',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('description', 'author', 'submitted_on',)

class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = ('post', 'author', 'vote_type', 'voted_on',)

class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = ('comment', 'author', 'vote_type', 'voted_on',)
   
