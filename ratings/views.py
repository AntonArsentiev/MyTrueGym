from constants import *
from .models import Rating
from django.shortcuts import render
from django.utils.translation import ugettext_lazy
from django.views.decorators.http import require_http_methods


@require_http_methods(ONLY_GET)
def index(request):
    context_data = {}
    if Rating.manager.all().count():
        for field in Rating.fields():
            max_field_row = Rating.manager.all().order_by(f"-{field}")[0]
            context_data[field] = [
                ugettext_lazy(field),
                getattr(max_field_row, field),
                max_field_row.athlete.first_name
            ]
        del context_data[ATHLETE]
    context = {
        DATA: context_data.values()
    }
    return render(request, "ratings/index.html", context=context)
