from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from reviews.models import Title, Category, Genre, Review
from api.serializers import (TitleSerializer, TitleReadSerializer,
                             CategorySerializer, GenreSerializer,
                             CommentSerializer, ReviewSerializer)

from api.permissions import IsAuthorOrModer, IsAdminOrReadOnly
from api.mixins import CustomViewSet
from api.filter import CustomFilter


class TitleViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter

    def get_queryset(self):
        queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModer,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        new_review = get_object_or_404(Review, pk=review_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, review=new_review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModer,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=self.get_title())
