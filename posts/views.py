from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET', 'POST'])
def ListAPIView(request):
    if request.method == 'GET':
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        data = serializer.data
        for post in data:
            item = Post.objects.get(id=post["id"])
            post["Upvotes"] = item.upvotes()
            post["Downvotes"] = item.downvotes()
        return Response(data)
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
    serialized_data["Votes"] = {
        "Upvotes": post.upvotes(),
        "Downvotes": post.downvotes()
    }

    comments = post.comment_set.all()
    serialized_data["Comments"] = CommentSerializer(comments, many=True).data
    

    return Response(serialized_data)

@api_view(['POST'])
def CommentAddAPIView(request, pk):
    post = Post.objects.get(id=pk)
    comment = Comment.objects.create(description=request.data.get('description'), author=request.user, post=post)
    serialized_data = CommentSerializer(comment, many=False)
    if request.data.get("description"):
        return Response(serialized_data.data)    

@api_view(['GET'])
def PostVoteAddAPIView(request, post_id, vote_type):
    post = Post.objects.get(id=post_id)
    if vote_type == 1:
        vote = PostVote.objects.create(post=post, author=request.user, vote_type=1)
    elif vote_type == 0:
        vote = PostVote.objects.create(post=post, author=request.user, vote_type=-1)

    return Response(PostVoteSerializer(vote, many=False).data)
