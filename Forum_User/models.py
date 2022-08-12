from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    # avatar = models.ImageField(upload_to="users/avatar", null=True, blank=True)
    # country = models.CharField(max_length=100, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile"


class Post(models.Model):
    title = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)
    location = models.TextField(null=True, blank=True)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username

    def comments(self):
        # TODO
        Comment.objects.filter(post=self)

    def get_upvotes(self):
        return Votes.objects.filter(upvote=True, post=self).count()

    def get_downvotes(self):
        return Votes.objects.filter(downvote=True, post=self).count()

    def is_voted(self):
        vote = None
        try:
            vote = Votes.objects.get(post=self, user=self.user)
        except:
            vote = None
        return vote

    class Meta:
        verbose_name = "Posts"
        verbose_name_plural = "Posts"


class ContentPost(models.Model):
    text_content = models.TextField(null=True, blank=True)
    post_media = models.ImageField(upload_to="post/images", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text_content

    class Meta:
        verbose_name = "Content Posts"
        verbose_name_plural = "Content Posts"


class Comment(models.Model):
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    comment_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Comments"
        verbose_name_plural = "Comments"


class Votes(models.Model):
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    vote_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vote_by.user.username

    class Meta:
        verbose_name = "Votes"
        verbose_name_plural = "Votes"

