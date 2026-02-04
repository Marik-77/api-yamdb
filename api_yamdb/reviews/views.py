from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from reviews.serializers import ReviewSerializer
from reviews.permissions import IsReviewAuthorOrReadOnly, IsAuthenticatedOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')).  # Импорт модели Tittle
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))    # Импорт модели Tittle
        serializer.save(author=self.request.user, title=title)