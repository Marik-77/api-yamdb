from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from api.filters import TitleFilter
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .permissions import IsAdmin, IsAdminOrReadOnly, IsUser, IsUserOrStaff
from reviews.models import Category, Genre, Review, Title, User
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        token = serializer.validated_data.get('token')
        if not serializer.validated_data.get('exists'):
            user = User.objects.create(username=username, email=email)
            token = default_token_generator.make_token(user)
        send_mail(
            subject='Registration',
            message=f'Здравствуйте {username}! '
                    f'Ваш код подтверждения: {token}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenApiView(generics.GenericAPIView):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = self.get_tokens_for_user(user)

        return Response(token, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)

        return {
            'token': str(refresh.access_token),
        }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=(IsUser,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        data = request.data.copy()
        if request.method == 'PATCH':
            data['role'] = request.user.role
            serializer = UserSerializer(
                user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CatGenreViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(CatGenreViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(CatGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-rating')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ['name', 'year', 'genre', 'category']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return TitleWriteSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsUserOrStaff,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = self.get_title()
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):

        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsUserOrStaff,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = self.get_review()
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):

        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                 title=self.kwargs.get('title_id'))
