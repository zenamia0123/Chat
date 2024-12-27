from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    website = models.URLField(null=True,blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='follower_user')
    following = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='following_user')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}'


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_user')
    image = models.ImageField(upload_to='post_image', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    description = models.TextField()
    hashtag = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    like = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} - {self.post}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment', null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_comment', null=True, blank=True)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_comment_like')
    comment = models.TextField(null=True, blank=True)
    like = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.like}'


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_story')
    image = models.ImageField(upload_to='story_image', null=True, blank=True)
    video = models.FileField(upload_to='story_vide', null=True, blank=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


class Saved(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_save')

    def __str__(self):
        return f'{self.user}'


class SaveItem(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='post_saveItem', null=True, blank=True)
    saved = models.ForeignKey(Saved, on_delete=models.CASCADE, related_name='saved_saveItem', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.saved}'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now=True)


class Massage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)



# .env \\\
# filter(hashtag), search(usernam   e), order(post(created_at))\\\
# translate(+2)\\\
# pagination--
# swagger\\\
# permission--
# jwt\\\
