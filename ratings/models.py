from constants import *
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.core.validators import MinValueValidator


class Rating(models.Model):
    run_60 = models.DecimalField(
        default=0.00,
        max_digits=5,
        decimal_places=2,
        verbose_name=ugettext_lazy("Бег на 60 м"),
        validators=[
            MinValueValidator(0.0)
        ],
        db_index=True
    )
    run_100 = models.DecimalField(
        default=0.00,
        max_digits=5,
        decimal_places=2,
        verbose_name=ugettext_lazy("Бег на 100 м"),
        validators=[
            MinValueValidator(0.0)
        ],
        db_index=True
    )
    run_3000 = models.DecimalField(
        default=0.00,
        max_digits=5,
        decimal_places=2,
        verbose_name=ugettext_lazy("Бег на 3000 м"),
        validators=[
            MinValueValidator(0.0)
        ],
        db_index=True
    )
    chin_ups = models.PositiveIntegerField(
        default=0,
        verbose_name=ugettext_lazy("Подтягивания"),
        db_index=True
    )
    push_ups = models.PositiveIntegerField(
        default=0,
        verbose_name=ugettext_lazy("Отжимания"),
        db_index=True
    )
    sit_ups = models.PositiveIntegerField(
        default=0,
        verbose_name=ugettext_lazy("Приседания"),
        db_index=True
    )
    squat = models.PositiveIntegerField(
        default=0,
        verbose_name=ugettext_lazy("Приседания со штангой"),
        db_index=True
    )
    bench_press = models.PositiveIntegerField(
        default=0,
        verbose_name=ugettext_lazy("Жим лежа со штангой"),
        db_index=True
    )
    dead_lift = models.PositiveIntegerField(
        default=0,
        verbose_name=ugettext_lazy("Тяга штанги от пола"),
        db_index=True
    )
    athlete = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Атлет",
        db_index=True
    )

    manager = models.Manager()

    def __str__(self):
        return self.athlete.username

    def context(self):
        return {
            RUN_60: self.run_60,
            RUN_100: self.run_100,
            RUN_3000: self.run_3000,
            CHIN_UPS: self.chin_ups,
            PUSH_UPS: self.push_ups,
            SIT_UPS: self.sit_ups,
            SQUAT: self.squat,
            BENCH_PRESS: self.bench_press,
            DEAD_LIFT: self.dead_lift,
            ATHLETE: self.athlete
        }

    @staticmethod
    def fields():
        return [
            RUN_60, RUN_100, RUN_3000,
            CHIN_UPS, PUSH_UPS, SIT_UPS,
            SQUAT, BENCH_PRESS, DEAD_LIFT,
            ATHLETE
        ]

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        ordering = [RUN_60]
