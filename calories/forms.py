from django import forms
from django.utils.translation import ugettext_lazy
from django.core.validators import MinValueValidator


class CalorieForm(forms.Form):
    title = forms.CharField(
        label=ugettext_lazy("Название"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Название")
            }
        ),
        required=False
    )
    kcal_from = forms.DecimalField(
        label=ugettext_lazy("Ккал от"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Ккал от"),
                "type": "number",
                "style": "width: 90px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    kcal_to = forms.DecimalField(
        label=ugettext_lazy("Ккал до"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Ккал до"),
                "type": "number",
                "style": "width: 90px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    protein_from = forms.DecimalField(
        label=ugettext_lazy("Белки от"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Белки от"),
                "type": "number",
                "style": "width: 110px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    protein_to = forms.DecimalField(
        label=ugettext_lazy("Белки до"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Белки до"),
                "type": "number",
                "style": "width: 110px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    oil_from = forms.DecimalField(
        label=ugettext_lazy("Жиры от"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Жиры от"),
                "type": "number",
                "style": "width: 90px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    oil_to = forms.DecimalField(
        label=ugettext_lazy("Жиры до"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Жиры до"),
                "type": "number",
                "style": "width: 90px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    carb_from = forms.DecimalField(
        label=ugettext_lazy("Углеводы от"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Углеводы от"),
                "type": "number",
                "style": "width: 120px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
    carb_to = forms.DecimalField(
        label=ugettext_lazy("Углеводы до"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ugettext_lazy("Углеводы до"),
                "type": "number",
                "style": "width: 120px;"
            }
        ),
        required=False,
        validators=[
            MinValueValidator(0.0)
        ]
    )
