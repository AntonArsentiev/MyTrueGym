from constants import *
from django import forms
from datetime import datetime
from ratings.models import Rating
from django.utils.translation import ugettext_lazy


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label=ugettext_lazy("Номер телефона"),
        min_length=12,
        max_length=20
    )
    password = forms.CharField(
        label=ugettext_lazy("Пароль"),
        max_length=16,
        widget=forms.PasswordInput()
    )


class SignUpForm1(forms.Form):
    day_choices = ((i + 1, str(i + 1)) for i in range(31))
    month_choices = (
        (1, ugettext_lazy("Январь")),
        (2, ugettext_lazy("Февраль")),
        (3, ugettext_lazy("Март")),
        (4, ugettext_lazy("Апрель")),
        (5, ugettext_lazy("Май")),
        (6, ugettext_lazy("Июнь")),
        (7, ugettext_lazy("Июль")),
        (8, ugettext_lazy("Август")),
        (9, ugettext_lazy("Сентябрь")),
        (10, ugettext_lazy("Октябрь")),
        (11, ugettext_lazy("Ноябрь")),
        (12, ugettext_lazy("Декабрь"))
    )
    year_choices = ((i, str(i)) for i in range(datetime.now().year, 1959, -1))
    gender_choices = (
        (1, ugettext_lazy("Мужской")),
        (2, ugettext_lazy("Женский"))
    )

    first_name = forms.CharField(
        label=ugettext_lazy("Имя"),
        min_length=4,
        max_length=20
    )
    last_name = forms.CharField(
        label=ugettext_lazy("Фамилия"),
        min_length=4,
        max_length=20
    )
    day = forms.ChoiceField(
        label=ugettext_lazy("День"),
        choices=day_choices
    )
    month = forms.ChoiceField(
        label=ugettext_lazy("Месяц"),
        choices=month_choices,
        widget=forms.Select(
            attrs={
                "onchange": "onMonthChange(this);"
            }
        )
    )
    year = forms.ChoiceField(
        label=ugettext_lazy("Год"),
        choices=year_choices,
        widget=forms.Select(
            attrs={
                "onchange": "onYearChange(this);"
            }
        )
    )
    gender = forms.ChoiceField(
        label=ugettext_lazy("Пол"),
        choices=gender_choices
    )


class SignUpForm2(forms.Form):
    country_region_choices = (
        ("+7", ugettext_lazy("Россия (+7)")),
        ("+380", ugettext_lazy("Украина (+380)")),
        ("+375", ugettext_lazy("Белорусь (+375)")),
        ("+77", ugettext_lazy("Казахстан (+77)")),
    )

    country_region = forms.ChoiceField(
        label=ugettext_lazy("Страна"),
        choices=country_region_choices,
        widget=forms.Select(
            attrs={
                "onchange": "onCountryRegionChange(this);"
            }
        )
    )
    phone_number = forms.CharField(
        label=ugettext_lazy("Номер телефона"),
        min_length=16,
        max_length=18,
        widget=forms.TextInput(
            attrs={
                "data-mask": "+0(000)000-00-00"
            }
        )
    )


class SignUpForm3(forms.Form):
    phone_number = forms.CharField(
        label=ugettext_lazy("Номер телефона"),
        min_length=16,
        max_length=18,
        disabled=True,
        required=False
    )
    code_for_phone_number = forms.CharField(
        label=ugettext_lazy("Код"),
        min_length=6,
        max_length=6
    )


class SignUpForm4(forms.Form):
    phone_number = forms.CharField(
        label=ugettext_lazy("Номер телефона"),
        min_length=16,
        max_length=18,
        disabled=True,
        required=False
    )
    code_for_phone_number = forms.CharField(
        label=ugettext_lazy("Код"),
        min_length=6,
        max_length=6,
        disabled=True,
        required=False
    )
    password = forms.CharField(
        label=ugettext_lazy("Пароль"),
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput()
    )


class SettingsForm(forms.Form):
    gender_choices = (
        (1, MALE),
        (2, FEMALE)
    )

    avatar = forms.ImageField(
        label=ugettext_lazy("Фотография"),
        widget=forms.FileInput(),
        required=False
    )
    first_name = forms.CharField(
        label=ugettext_lazy("Имя"),
        min_length=4,
        max_length=20
    )
    last_name = forms.CharField(
        label=ugettext_lazy("Фамилия"),
        min_length=4,
        max_length=20
    )
    email = forms.EmailField(
        label=ugettext_lazy("Почта"),
        required=False
    )
    phone_number = forms.CharField(
        label=ugettext_lazy("Номер телефона"),
        max_length=18,
        min_length=16
    )


class AchievementsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            RUN_60, RUN_100, RUN_3000,
            CHIN_UPS, PUSH_UPS, SIT_UPS,
            SQUAT, BENCH_PRESS, DEAD_LIFT
        ]
