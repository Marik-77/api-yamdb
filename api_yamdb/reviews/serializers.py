from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field = 'user_name',
        read_only = True,
        default = serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators = [
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть больше 10')
        ]
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_field = ('id', 'author', 'pub_date') # уточнить поля

    def validate(self, data):
        """
        Проверка отзыва.
        
        Проверят, что пользователь оставил только один отзыв
        на произведение.
        """

        request = self.context.get('request')
        view = self.context.get('view')

        if request and view and request.method == 'POST':
            title_id = view.kwargs.get('title_id')
            user = request.user
            if Review.objects.filter(title_id=title_id, author=user).exists(): #???
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение'
                )
        return data