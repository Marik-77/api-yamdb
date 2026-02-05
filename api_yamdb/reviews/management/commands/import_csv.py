import os

from django.core.management.base import BaseCommand
import pandas as pd

from reviews.models import Category, Genre, Title, Review, Comment, User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        directory_path = kwargs['path']

        files = {
            'users.csv': self.import_users,
            'category.csv': self.import_categories,
            'genre.csv': self.import_genres,
            'titles.csv': self.import_titles,
            'review.csv': self.import_reviews,
            'comments.csv': self.import_comments,
        }

        for filename, func in files.items():
            file_path = os.path.join(directory_path, filename)

            if os.path.exists(file_path):
                print(f'Импортирую {filename}')
                try:
                    func(file_path)
                    print(f'{filename} импортирован')
                except Exception as e:
                    print(f'Ошибка при импорте {filename}: {e}')
            else:
                print(f'Файл {filename} не найден в директории')

    def import_users(self, file_path):
        users = []
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            users.append(User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row.get('role', 'user'),
                bio=row.get('bio', ''),
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', '')
            ))
        User.objects.bulk_create(users)

    def import_categories(self, file_path):
        df = pd.read_csv(file_path)
        categories = []
        for _, row in df.iterrows():
            categories.append(Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            ))
        Category.objects.bulk_create(categories)

    def import_genres(self, file_path):
        df = pd.read_csv(file_path)
        genres = []
        for row in df.iterrows():
            genres.append(Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            ))
        Genre.objects.bulk_create(genres)

    def import_titles(self, file_path):
        df = pd.read_csv(file_path)
        titles = []
        for _, row in df.iterrows():
            category = Category.objects.get(id=row['category'])
            titles.append(Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category
            ))
        Title.objects.bulk_create(titles)

    def import_reviews(self, file_path):
        df = pd.read_csv(file_path)
        reviews = []
        for _, row in df.iterrows():
            title = Title.objects.get(id=row['title_id'])
            author = User.objects.get(id=row['author'])
            reviews.append(Review(
                id=row['id'],
                title=title,
                text=row['text'],
                author=author,
                score=int(row['score']),
                pub_date=row['pub_date']
            ))
        Review.objects.bulk_create(reviews)

    def import_comments(self, file_path):
        df = pd.read_csv(file_path)
        comments = []
        for _, row in df.iterrows():
            review = Review.objects.get(id=row['review_id'])
            author = User.objects.get(id=row['author'])
            comments.append(Comment(
                id=row['id'],
                review=review,
                text=row['text'],
                author=author,
                pub_date=row['pub_date']
            ))
        Comment.objects.bulk_create(comments)
