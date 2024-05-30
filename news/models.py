from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.DecimalField(default=0, decimal_places=2, max_digits=5)

    def update_rating(self):
        posts_rate = self.post_set.aggregate(postRaiting=Sum('rating'))
        p_rate = 0
        p_rate += posts_rate.get('postRaiting')

        comments_rate = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        c_rate = 0
        c_rate += comments_rate.get('commentRating')

        self.authorRating = p_rate * 3 + c_rate
        self.save()

        class Meta:
            verbose_name = 'Автор'
            verbose_name_plural = 'Авторы'

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    )

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    date_created = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self):  # Методы лайк дизлайк
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def prewiew(self):  # Превью
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class PostCategory(models.Model):  # Модель для связи многие к многим
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):  # Методы лайк дизлайк
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriber',
    )