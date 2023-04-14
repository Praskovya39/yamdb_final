from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from django.conf import settings
from reviews.validator import year_validate
from api_yamdb.settings import MIN_SCORE, MAX_SCORE


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Указать название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(year_validate,),
        help_text='Указать год выпуска'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Краткое описание произведения'
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Указать жанр'
    )
    category = models.ForeignKey(
        'Category',
        blank=True,
        on_delete=models.PROTECT,
        related_name='titles',
        verbose_name='Категория',
        help_text='Указать категорию'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Категория',
        help_text='Указать название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг категории',
        help_text='Указать слаг категории'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Жанр',
        help_text='Указать название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг жанра',
        help_text='Указать слаг жанра'
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв по произведению',
        help_text='Укажите произведение'
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Напишите Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        help_text='Тот, кто оставил отзыв'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        help_text='Укажите рейтинг',
        validators=(MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE))
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text='Укажите дату',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:settings.LEN_OUTPUT]


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий к отзыву'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Укажите комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.LEN_OUTPUT]
