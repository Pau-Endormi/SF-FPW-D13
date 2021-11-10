from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def update_rating(self):
        post = self.post_set.aggregate(postRating=Sum("rating"))
        postR = 0
        postR += post.get("postRating")

        comment = self.user.comment_set.aggregate(commentRating=Sum("rating"))
        commentR = 0
        commentR += comment.get("commentRating")

        self.rating = postR*3 + commentR
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('post_category', kwargs={'pk': self.id})


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ARTICLE = "AR"
    NEWS = "NE"
    TYPE = [
        (ARTICLE, "Статья"),
        (NEWS, "Новость")
    ]
    type = models.CharField(max_length=2, choices=TYPE, default=ARTICLE)
    timeCreation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:125] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.post)} > category: «{str(self.category)}»'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timeCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.post)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
