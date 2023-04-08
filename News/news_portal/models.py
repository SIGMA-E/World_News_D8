from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    rating_autor = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        sum_rating_post = Post.objects.filter(author=self.id).values('rating_post')
        total_rating_post = sum([i['rating_post'] for i in sum_rating_post])

        sum_rating_comment = Comment.objects.filter(user=self.id).values('rating_comment')
        total_rating_comment = sum([i['rating_comment'] for i in sum_rating_comment])

        sum_rating_comment_post = Comment.objects.filter(post__author__id=self.id).values('rating_comment')
        total_rating_comment_post = sum([i['rating_comment'] for i in sum_rating_comment_post])

        self.rating_autor = total_rating_post * 3 + total_rating_comment + total_rating_comment_post
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    article = 'ar'
    news = 'nw'

    SELECT = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    type_post = models.CharField(max_length=2, choices=SELECT)
    time_post = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default='Заголовок', unique=True)
    text_post = models.TextField(default='текст статьи, новости')
    rating_post = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[:124]}...'

    def __str__(self):
        return f'{self.time_post} {self.rating_post}'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    text_comment = models.TextField(blank=True)
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
