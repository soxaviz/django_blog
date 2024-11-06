from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import display
from django.utils.safestring import mark_safe


# Create your models here.

# Category => blog_app_category

# category
# id
# name varchar(100)

# Модель = таблица в БД


class Category(models.Model):
    # pk
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # название класса в единственном числе
        verbose_name_plural = 'Категории'  # название класса во множественном числе


# python manage.py makemigrations - создание файла с историей работы с таблицей
# python manage.py migrate


class HomeSlider(models.Model):
    photo = models.ImageField(upload_to='home_slider/%Y/%m/%d/',
                              verbose_name='Фото',
                              help_text='Можно добавить только фото формата png')
    title = models.CharField(max_length=100, verbose_name='Заголовок слайда',
                             help_text='Будь аккуратнее бразе')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'


class FAQ(models.Model):
    question = models.CharField(max_length=100, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


# python manage.py makemigrations
# python manage.py migrate


class Post(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', unique=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    preview = models.ImageField(upload_to='posts/%Y/%m/%d/', null=True, blank=True,
                                verbose_name='Фото')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.name

    # from django.contrib.admin import display
    # from django.utils.safestring import mark_safe

    #
    @display()
    def display_gallery_images(self):
        photos = self.postgallery_set.all()
        photos_block_start = '<div style="display: flex; gap: 30px">'
        photos_block_end = '</div>'
        images_tags = ''

        for photo in photos:
            images_tags += f'<img src="{photo.image.url}" width="70" height="70">'
        result = photos_block_start + images_tags + photos_block_end
        return mark_safe(result)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

# 1,2,3
# 3,2,1

# media -> post-post_id -> gallery ->


def post_gallery_image_path(instance, filename):
    return f'post-{instance.post.id}/gallery/{filename}'


# post-2/gallery/post-1.jpg

class PostGallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    image = models.ImageField(upload_to=post_gallery_image_path, verbose_name='Фото')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Пост-{self.post}: {self.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostViewsCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=150)


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')


class Dislike(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')



# спорт -> 5 статей

# статья про спортивные события
# statya-pro-sport
