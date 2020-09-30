from constants import *
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Calorie(models.Model):
    title = models.CharField(
        default="",
        max_length=20,
        verbose_name="Название",
        db_index=False
    )
    title_en = models.CharField(
        default="",
        max_length=20,
        verbose_name="Title",
        db_index=False
    )
    avatar = models.ImageField(
        verbose_name="Фотография"
    )
    kcal = models.PositiveIntegerField(
        default=0,
        verbose_name="Ккал",
        db_index=False,
        validators=[
            MinValueValidator(MIN_CALORIES_VALUE),
            MaxValueValidator(MAX_CALORIES_VALUE)
        ]
    )
    protein = models.DecimalField(
        default=0.0,
        max_digits=5,
        decimal_places=2,
        verbose_name="Белки",
        db_index=False,
        validators=[
            MinValueValidator(MIN_CALORIES_VALUE),
            MaxValueValidator(MAX_CALORIES_VALUE)
        ]
    )
    oil = models.DecimalField(
        default=0.0,
        max_digits=5,
        decimal_places=2,
        verbose_name="Жиры",
        db_index=False,
        validators=[
            MinValueValidator(MIN_CALORIES_VALUE),
            MaxValueValidator(MAX_CALORIES_VALUE)
        ]
    )
    carb = models.DecimalField(
        default=0.0,
        max_digits=5,
        decimal_places=2,
        verbose_name="Углеводы",
        db_index=False,
        validators=[
            MinValueValidator(MIN_CALORIES_VALUE),
            MaxValueValidator(MAX_CALORIES_VALUE)
        ]
    )

    manager = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Калория"
        verbose_name_plural = "Калории"
        ordering = [KCAL]
        indexes = [
            models.Index(fields=[TITLE_EN, KCAL, PROTEIN, OIL, CARB]),
            models.Index(fields=[TITLE, KCAL, PROTEIN, OIL, CARB]),
        ]
