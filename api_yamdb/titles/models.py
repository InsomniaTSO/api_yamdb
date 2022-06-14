from django.db import models

from users.models import User

SCORE_CHOICES = (
    (1, 1), (2, 2),
    (3, 3), (4, 4),
    (5, 5), (6, 6),
    (7, 7), (8, 8),
    (9, 9), (10, 10)
)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return self.name[:10]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateField(
        auto_now_add=True,
        db_index=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateField(
        auto_now_add=True,
        db_index=True
    )
