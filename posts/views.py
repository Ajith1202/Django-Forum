from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET',])
def ListAPIView(request):
    queryset = Post.objects.all()
    serializer = PostSerializer(queryset, many=True)
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