from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET', 'POST'])
def ListAPIView(request):
    if request.method == 'GET':
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        post = Post.objects.create(title=title, description=description, author=request.user)
        serializer = PostSerializer(post, many=False)
        
        return Response(serializer.data)  

@api_view(['GET'])
def DetailAPIView(request, pk):
    post = Post.objects.get(id=pk)
    serialized_data = PostSerializer(post, many=False).data
    
    post_votes = post.post_vote.all()
    serialized_data["votes"] = PostVoteSerializer(post_votes, many=True).data

    comments = post.comment_set.all()
    serialized_data["comments"] = CommentSerializer(comments, many=True).data
    

    return Response(serialized_data)

@api_view(['POST'])
def CommentAddAPIView(request, pk):
    post = Post.objects.get(id=pk)
    comment = Comment.objects.create(description=request.data.get('description'), author=request.user, post=post)
    serialized_data = CommentSerializer(comment, many=False)
    if request.data.get("description"):
        return Response(serialized_data.data)    

        