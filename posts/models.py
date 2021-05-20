from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return (str(self.title) + " by " + str(self.author.username))

    def increment_view(self):
        self.view_count = self.view_count + 1

    def upvotes(self):
        queryset = self.post_vote.all()
        queryset = [i.vote_type for i in queryset if i.vote_type == 1]
        return len(queryset)

    def downvotes(self):
        queryset = self.post_vote.all()
        queryset = [i.vote_type for i in queryset if i.vote_type == -1]
        return len(queryset)
    
    def vote_score(self):
        queryset = self.post_vote.all()
        queryset = [i.vote_type for i in queryset]
        return sum(queryset)
    

class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_vote")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ))
    voted_on = models.DateTimeField(auto_now_add=True)