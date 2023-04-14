from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from reviews.models import Title, Category, Genre, Comment, Review
from api_yamdb.settings import MIN_SCORE, MAX_SCORE
from reviews.validator import year_validate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    year = serializers.IntegerField(
        validators=(year_validate,)
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return Review.objects.filter(title=obj).aggregate(
            Avg('score')).get('score__avg')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(
                MIN_SCORE, f'Оценка не может быть менее {MIN_SCORE}'
            ),
            MaxValueValidator(
                MAX_SCORE, f'Оценка не божет быть более {MAX_SCORE}'
            )
        )
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        reviewer = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        if Review.objects.filter(author=reviewer, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Оставлять отзыв на одно произведение дважды запрещено!'
            )
        return data
