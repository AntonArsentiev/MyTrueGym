from .forms import *
from .models import *
from constants import *
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.utils.translation import get_language, ugettext_lazy


@require_http_methods(GET_AND_POST)
def index(request):
    if request.method == GET:
        calories = Calorie.manager.all()
        calorie_form = CalorieForm()
        context = {
            ITEMS: calories,
            FORM: calorie_form
        }
        return render(request, "calories/index.html", context=context)
    else:
        if request.POST.get(CLEAR) is not None:
            return redirect("calories-index")

        form = CalorieForm(request.POST)
        if form.is_valid():
            if request.POST.get(FIND) is not None:
                find_query = CALORIES_FIND_TEMPLATE.format(
                    request.POST.get(TITLE).strip(),
                    request.POST.get(KCAL_FROM).strip(),
                    request.POST.get(KCAL_TO).strip(),
                    request.POST.get(PROTEIN_FROM).strip(),
                    request.POST.get(PROTEIN_TO).strip(),
                    request.POST.get(OIL_FROM).strip(),
                    request.POST.get(OIL_TO).strip(),
                    request.POST.get(CARB_FROM).strip(),
                    request.POST.get(CARB_TO).strip(),
                )

                if len(find_query) != 8:
                    return redirect("find/{}/".format(find_query))

        form = CalorieForm(initial=request.POST)
        calories = Calorie.manager.all()
        context = {
            FORM: form,
            ITEMS: calories,
            ERROR: ugettext_lazy("Пожалуйста проверяйте корректность вводимых данных")
        }
        return render(request, "calories/index.html", context=context)


@require_http_methods(ONLY_GET)
def find_by_query(request, query):
    query_data = query.split("-")
    data_valid = True

    for i in range(4):  # kcal, protein, oil, carb
        if query_data[2 * i + 1] and query_data[2 * i + 2] and int(query_data[2 * i + 1]) > int(query_data[2 * i + 2]):
            data_valid = False
            break

    if data_valid:
        # kcal
        kcal_gte = query_data[1] if query_data[1] else MIN_CALORIES_VALUE
        kcal_lte = query_data[2] if query_data[2] else MAX_CALORIES_VALUE

        # protein
        protein_gte = query_data[3] if query_data[3] else MIN_CALORIES_VALUE
        protein_lte = query_data[4] if query_data[4] else MAX_CALORIES_VALUE

        # oil
        oil_gte = query_data[5] if query_data[5] else MIN_CALORIES_VALUE
        oil_lte = query_data[6] if query_data[6] else MAX_CALORIES_VALUE

        # carb
        carb_gte = query_data[7] if query_data[7] else MIN_CALORIES_VALUE
        carb_lte = query_data[8] if query_data[8] else MAX_CALORIES_VALUE

        # title
        title = query_data[0] if query_data[0] else ANY_TITLE

        if get_language() == LANGUAGE_EN:
            items = Calorie.manager.filter(
                title_en__istartswith=title,
                kcal__gte=kcal_gte,
                kcal__lte=kcal_lte,
                protein__gte=protein_gte,
                protein__lte=protein_lte,
                oil__gte=oil_gte,
                oil__lte=oil_lte,
                carb__gte=carb_gte,
                carb__lte=carb_lte
            )
        else:
            items = Calorie.manager.filter(
                title__istartswith=title,
                kcal__gte=kcal_gte,
                kcal__lte=kcal_lte,
                protein__gte=protein_gte,
                protein__lte=protein_lte,
                oil__gte=oil_gte,
                oil__lte=oil_lte,
                carb__gte=carb_gte,
                carb__lte=carb_lte
            )
    else:
        items = Calorie.manager.all()

    initial = {
        TITLE: query_data[0],
        KCAL_FROM: query_data[1],
        KCAL_TO: query_data[2],
        PROTEIN_FROM: query_data[3],
        PROTEIN_TO: query_data[4],
        OIL_FROM: query_data[5],
        OIL_TO: query_data[6],
        CARB_FROM: query_data[7],
        CARB_TO: query_data[8]
    }
    error = NONE
    if not data_valid:
        error = ugettext_lazy("Пожалуйста проверяйте корректность вводимых данных")
    calorie_form = CalorieForm(initial=initial)
    context = {
        ITEMS: items,
        FORM: calorie_form,
        ERROR: error
    }
    return render(request, "calories/index.html", context=context)
