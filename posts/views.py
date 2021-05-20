from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


# LIST ALL THE QUESTIONS , ADD A QUESTION
@api_view(['GET', 'POST'])
def ListAPIView(request):
    if request.method == 'GET':    # GET REQUEST
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        data = serializer.data
        for post in data:
            item = Post.objects.get(id=post["id"])    # FOR ACCESSING EACH POST
            post["Upvotes"] = item.upvotes()
            post["Downvotes"] = item.downvotes()
        return Response(data)
    elif request.method == 'POST':    # POST REQUEST
        title = request.data.get('title')
        description = request.data.get('description')
        post = Post.objects.create(title=title, description=description, author=request.user)    # THE CURRENT USER WILL BE THE AUTHOR.
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


# DETAILED VIEW OF A QUESTION , UPDATE A QUESTION
@api_view(['GET', 'PUT'])
def DetailAPIView(request, pk):
    # TRY-EXCEPT CLAUSE IN-CASE THE QUESTION DOES NOT EXIST
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized_data = PostSerializer(post, many=False).data
    comments = post.comment_set.all()    # FETCHING ALL THE COMMENTS OF THE GIVEN POST
    serialized_data["Comments"] = CommentSerializer(comments, many=True).data
    serialized_data["Votes"] = {
            "Upvotes": post.upvotes(),
            "Downvotes": post.downvotes()
        }

    if request.method == 'POST':    # POST REQUEST
        serialized_data["Votes"] = {
            "Upvotes": post.upvotes(),
            "Downvotes": post.downvotes()
        }
        return Response(serialized_data)
    elif request.method == 'PUT':    # PUT REQUEST
        if post.author == request.user:    # ONLY ALLOW UPDATION BY THE AUTHOR OF THE QUESTION
            serialized_data = PostSerializer(post, data=request.data, many=False)
            if serialized_data.is_valid():
                serialized_data.save()
                serialized_data = serialized_data.data
            serialized_data["Votes"] = {
                "Upvotes": post.upvotes(),
                "Downvotes": post.downvotes()
            }
            serialized_data["Comments"] = CommentSerializer(comments, many=True).data
            return Response(serialized_data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)    # IF ANY OTHER USER OTHER THAN THE AUTHOR TRIES TO UPDATE A QUESTION    

    return Response(serialized_data)


# ADD COMMENTS TO QUESTIONS
@api_view(['GET', 'POST'])
def CommentAddAPIView(request, pk):
    # TRY-EXCEPT CLAUSE IN-CASE THE QUESTION DOES NOT EXIST
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    comment = Comment.objects.create(description=request.data.get('description'), author=request.user, post=post)
    serialized_data = CommentSerializer(comment, many=False)
    if request.data.get("description"):
        return Response(serialized_data.data)    
    return Response("Add content for your comment!!!")    # IF NO DESCRIPTION IS GIVEN FOR THE COMMENT


# UPVOTE OR DOWNVOTE A QUESTION
@api_view(['GET'])
def PostVoteAddAPIView(request, post_id, vote_type):
    # TRY-EXCEPT CLAUSE IN-CASE THE QUESTION DOES NOT EXIST
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.user.is_authenticated:
        content = {"Login to your account."}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    if vote_type == 1:    # UPVOTE 
        vote = PostVote.objects.create(post=post, author=request.user, vote_type=1)
    elif vote_type == 0:    # DOWNVOTE
        vote = PostVote.objects.create(post=post, author=request.user, vote_type=-1)

    return Response(PostVoteSerializer(vote, many=False).data)


# DELETE A QUESTION 
@api_view(['DELETE'])
def PostDeleteAPIView(request, pk):
    # TRY-EXCEPT CLAUSE IN-CASE THE QUESTION DOES NOT EXIST
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.author == request.user:    # ONLY THE AUTHOR IS ALLOWED TO DELETE HIS/HER QUESTION
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)    # IF ANY OTHER USER ATTEMPTS TO DELETE A QUESTION

