from constants import *
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy


class Sportsman(models.Model):
    gender_choices = (
        (1, MALE),
        (2, FEMALE)
    )

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=20,
        db_index=True
    )
    gender = models.CharField(
        verbose_name="Пол",
        choices=gender_choices,
        max_length=1
    )
    birthday = models.DateField(
        verbose_name="Дата рождения"
    )
    athlete = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Атлет"
    )
    avatar = models.ImageField(
        verbose_name="Фотография"
    )
    email_is_verified = models.BooleanField(
        verbose_name="Подтверждена почта",
        default=False
    )

    manager = models.Manager()

    def __str__(self):
        return self.phone_number

    def context(self):
        return {
            ugettext_lazy("Номер телефона"): self.phone_number,
            ugettext_lazy("Пол"): self.gender,
            AVATAR: self.avatar
        }

    class Meta:
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"
        ordering = [PHONE_NUMBER]
