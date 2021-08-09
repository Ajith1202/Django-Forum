from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return (str(self.title) + " by " + str(self.author.username))       # FOR THE ADMIN PANEL

    def increment_view(self, curr_user):       # ANYTIME A POST IS VIEWED, THIS METHOD GETS CALLED.
        if self.author != curr_user:
            self.view_count = self.view_count + 1

    def votes(self):        # RETURNS THE NUMBER OF UPVOTES AND DOWNVOTES OF A POST, AS A TUPLE
        queryset = self.post_vote.all()
        a, b = 0, 0
        for i in queryset:
            if i.vote_type == 1:
                a += 1
            if i.vote_type == -1:
                b += 1
        return (a, b)

    def vote_score(self):       # RETURNS (UPVOTES - DOWNVOTES) OF A POST
        queryset = self.post_vote.all()
        queryset = [i.vote_type for i in queryset]
        return sum(queryset)


class Comment(models.Model):
    description = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE) # PARENT FIELD, FOR REPLIES

    submitted_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description

    def children(self):
        return Comment.objects.filter(parent=self)      # RETURNS THE CHILDREN OF THE COMMENT

    @property
    def is_parent(self):    # RETURNS IF THE COMMENT IS A TOP-LEVEL COMMENT OR NOT
        if self.parent is None:
            return True
        return False

class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_vote")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ))
    voted_on = models.DateTimeField(auto_now_add=True)
