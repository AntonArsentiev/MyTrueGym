from .tasks import *
from .forms import *
from .models import *
from constants import *
from datetime import datetime
from ratings.models import Rating
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy, activate
from django.views.decorators.http import require_http_methods


@require_http_methods(ONLY_GET)
def index(request):
    return redirect("sportsmen-info") if request.user.is_authenticated else render(request, "sportsmen/index.html")


@require_http_methods(ONLY_GET)
def sportsmen_info(request):
    rating = Rating.manager.get(pk=request.user.pk)
    sportsman = Sportsman.manager.get(pk=request.user.pk)
    sportsman_context = sportsman.context()
    gender = ugettext_lazy("Пол")
    if sportsman_context[gender] == "1":
        sportsman_context[gender] = ugettext_lazy("Мужской")
    else:
        sportsman_context[gender] = ugettext_lazy("Женский")

    email_message = NONE
    if sportsman.athlete.email and not sportsman.email_is_verified:
        email_message = ugettext_lazy("Для подтверждения почты перейдите по указанному вами адресу")

    email_message_verified = NONE
    if request.COOKIES.get(SETTINGS_COOKIE_EMAIL_VERIFIED, IS_NOT_OK) == IS_OK:
        email_message_verified = ugettext_lazy("Почтовый адрес успешно подтвержден")

    rating_data = {}
    for key, value in rating.context().items():
        rating_data[ugettext_lazy(key)] = value

    context = {
        RATING_DATA: rating_data.items(),
        SPORTSMAN_DATA: sportsman_context.items(),
        USER_DATA: {
            ugettext_lazy("Имя"): sportsman.athlete.first_name,
            ugettext_lazy("Фамилия"): sportsman.athlete.last_name,
            ugettext_lazy("Почта"): sportsman.athlete.email if sportsman.email_is_verified else "",
        }.items(),
        EMAIL_MESSAGE: email_message,
        EMAIL_MESSAGE_VERIFIED: email_message_verified
    }

    response = render(request, "sportsmen/info.html", context=context)
    response.set_cookie(SETTINGS_COOKIE_EMAIL_VERIFIED, IS_NOT_OK, max_age=SIGN_UP_PAGE_COOKIE_AGE)
    return response


@require_http_methods(ONLY_GET)
def sportsmen_lang(request, lang):
    activate(lang)
    response = redirect(request.META[HTTP_REFERER])
    response.set_cookie(DJANGO_LANGUAGE, lang)
    return response


def page_400(request, exception):
    return render(request, "sportsmen/400.html")


def page_403(request, exception):
    return render(request, "sportsmen/403.html")


def page_404(request, exception):
    return render(request, "sportsmen/404.html")


def page_500(request):
    return render(request, "sportsmen/500.html")


@require_http_methods(GET_AND_POST)
def login(request):
    if request.method == GET:
        has_error, error = request.COOKIES.get(LOGIN_COOKIE_ERROR, IS_OK), NONE
        if has_error == IS_NOT_OK:
            error = ugettext_lazy("Проверьте корректность введенных данных")

        login_form = LoginForm()
        context = {
            FORM: login_form,
            ERROR: error
        }
        response = render(request, "sportsmen/login.html", context=context)
        response.set_cookie(
            LOGIN_COOKIE_ERROR,
            IS_OK,
            max_age=SIGN_UP_PAGE_COOKIE_AGE
        )
        return response
    elif request.method == POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                sportsman = Sportsman.manager.get(phone_number=form.cleaned_data[PHONE_NUMBER])
                password = form.cleaned_data[PASSWORD]
                user = authenticate(request, username=sportsman.pk, password=password)
                if user is not None:
                    log_in(request, user)
                    return redirect("sportsmen-index")
            except ObjectDoesNotExist:
                pass
        response = redirect("login")
        response.set_cookie(
            LOGIN_COOKIE_ERROR,
            IS_NOT_OK,
            max_age=SIGN_UP_PAGE_COOKIE_AGE
        )
        return response


@require_http_methods(ONLY_GET)
def logout(request):
    log_out(request)
    return redirect("sportsmen-index")


@require_http_methods(GET_AND_POST)
def signup(request):
    sign_up_page = request.COOKIES.get(SIGN_UP_PAGE, SIGN_UP_PAGE_FIRST)
    sign_up_get_form = SignUpForm1() if sign_up_page == SIGN_UP_PAGE_FIRST \
        else SignUpForm2() if sign_up_page == SIGN_UP_PAGE_SECOND \
        else SignUpForm3() if sign_up_page == SIGN_UP_PAGE_THIRD \
        else SignUpForm4()

    if request.method == GET:
        sign_up_stage_page = ugettext_lazy("Регистрация - этап {}")
        sign_up_stage_page = sign_up_stage_page.format(sign_up_page)
        submit_value = ugettext_lazy("Далее")
        has_error, error = request.COOKIES.get(SIGN_UP_COOKIE_ERROR, IS_OK), NONE
        if sign_up_page == SIGN_UP_PAGE_SECOND:
            sign_up_get_form.fields[PHONE_NUMBER].initial = "+7"
            submit_value = ugettext_lazy("Получить код")
            if has_error == IS_NOT_OK:
                error = ugettext_lazy("Уже существует аккаунт с таким номером телефона или номер телефона некорректен")
        elif sign_up_page == SIGN_UP_PAGE_THIRD:
            sign_up_get_form.fields[PHONE_NUMBER].initial = request.COOKIES.get(SIGN_UP_COOKIE_PHONE_NUMBER)
            submit_value = ugettext_lazy("Подтвердить код")
            if has_error == IS_NOT_OK:
                error = ugettext_lazy("Введенный код не подтвержден")
        elif sign_up_page == SIGN_UP_PAGE_FOURTH:
            sign_up_get_form.fields[PHONE_NUMBER].initial = request.COOKIES.get(SIGN_UP_COOKIE_PHONE_NUMBER)
            sign_up_get_form.fields[CODE_FOR_PHONE_NUMBER].initial = request.COOKIES.get(SIGN_UP_COOKIE_PHONE_NUMBER_CODE)
            submit_value = ugettext_lazy("Создать аккаунт")
        context = {
            FORM: sign_up_get_form,
            STAGE: sign_up_stage_page,
            SUBMIT_VALUE: submit_value,
            ERROR: error
        }
        response = render(request, "sportsmen/signup.html", context=context)
        response.set_cookie(SIGN_UP_COOKIE_ERROR, IS_OK, max_age=SIGN_UP_PAGE_COOKIE_AGE)
        return response
    elif request.method == POST:
        sign_up_post_form = SignUpForm1(request.POST) if sign_up_page == SIGN_UP_PAGE_FIRST \
                        else SignUpForm2(request.POST) if sign_up_page == SIGN_UP_PAGE_SECOND \
                        else SignUpForm3(request.POST) if sign_up_page == SIGN_UP_PAGE_THIRD \
                        else SignUpForm4(request.POST)
        
        if sign_up_page == SIGN_UP_PAGE_FIRST:
            if sign_up_post_form.is_valid():
                response = redirect("signup")
                response.set_cookie(
                    SIGN_UP_PAGE,
                    SIGN_UP_PAGE_SECOND,
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                response.set_cookie(
                    SIGN_UP_COOKIE_FIRST_NAME,
                    "|".join(str(ord(element)) for element in sign_up_post_form.cleaned_data[FIRST_NAME]),
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                response.set_cookie(
                    SIGN_UP_COOKIE_LAST_NAME,
                    "|".join(str(ord(element)) for element in sign_up_post_form.cleaned_data[LAST_NAME]),
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                response.set_cookie(
                    SIGN_UP_COOKIE_DAY,
                    sign_up_post_form.cleaned_data[DAY],
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                response.set_cookie(
                    SIGN_UP_COOKIE_MONTH,
                    sign_up_post_form.cleaned_data[MONTH],
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                response.set_cookie(
                    SIGN_UP_COOKIE_YEAR,
                    sign_up_post_form.cleaned_data[YEAR],
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                response.set_cookie(
                    SIGN_UP_COOKIE_GENDER,
                    sign_up_post_form.cleaned_data[GENDER],
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                return response
        elif sign_up_page == SIGN_UP_PAGE_SECOND:
            response = redirect("signup")

            is_valid, country_region, phone_number = True, request.POST.get(COUNTRY_REGION), request.POST.get(PHONE_NUMBER)
            if (country_region == "+380" and len(phone_number) < 18) or \
               (country_region == "+375" and len(phone_number) < 17) or \
               (country_region == "+77" and len(phone_number) < 16) or \
               (country_region == "+7" and len(phone_number) < 16):
                is_valid = False

            if sign_up_post_form.is_valid() and is_valid:
                try:
                    Sportsman.manager.get(phone_number=sign_up_post_form.cleaned_data[PHONE_NUMBER])
                    response.set_cookie(
                        SIGN_UP_COOKIE_ERROR,
                        IS_NOT_OK,
                        max_age=SIGN_UP_PAGE_COOKIE_AGE
                    )
                    return response
                except ObjectDoesNotExist:
                    response.set_cookie(
                        SIGN_UP_PAGE,
                        SIGN_UP_PAGE_THIRD,
                        max_age=SIGN_UP_PAGE_COOKIE_AGE
                    )
                    response.set_cookie(
                        SIGN_UP_COOKIE_PHONE_NUMBER,
                        sign_up_post_form.cleaned_data[PHONE_NUMBER],
                        max_age=SIGN_UP_PAGE_COOKIE_AGE
                    )

                    send_code_to_activate_phone_number.delay(sign_up_post_form.cleaned_data[PHONE_NUMBER])

                    return response
            response.set_cookie(
                SIGN_UP_COOKIE_ERROR,
                IS_NOT_OK,
                max_age=SIGN_UP_PAGE_COOKIE_AGE
            )
            return response

        elif sign_up_page == SIGN_UP_PAGE_THIRD:
            if sign_up_post_form.is_valid():
                code_for_phone_number = sign_up_post_form.cleaned_data[CODE_FOR_PHONE_NUMBER]
                phone_number = request.COOKIES.get(SIGN_UP_COOKIE_PHONE_NUMBER)
                phone_number_verified = send_code_to_verify_phone_number(phone_number, code_for_phone_number)
                response = redirect("signup")

                if phone_number_verified:
                    response.set_cookie(
                        SIGN_UP_PAGE,
                        SIGN_UP_PAGE_FOURTH,
                        max_age=SIGN_UP_PAGE_COOKIE_AGE
                    )
                    response.set_cookie(
                        SIGN_UP_COOKIE_PHONE_NUMBER_CODE,
                        code_for_phone_number,
                        max_age=SIGN_UP_PAGE_COOKIE_AGE
                    )
                else:
                    response.set_cookie(
                        SIGN_UP_COOKIE_ERROR,
                        IS_NOT_OK,
                        max_age=SIGN_UP_PAGE_COOKIE_AGE
                    )
                return response
        elif sign_up_page == SIGN_UP_PAGE_FOURTH:
            if sign_up_post_form.is_valid():
                first_name_cookie = request.COOKIES.get(SIGN_UP_COOKIE_FIRST_NAME).split("|")
                last_name_cookie = request.COOKIES.get(SIGN_UP_COOKIE_LAST_NAME).split("|")
                first_name_cookie = [int(element) for element in first_name_cookie if element]
                last_name_cookie = [int(element) for element in last_name_cookie if element]

                user = User()
                user.save()
                user.username = user.pk
                user.first_name = "".join(map(chr, first_name_cookie))
                user.last_name = "".join(map(chr, last_name_cookie))
                user.set_password(sign_up_post_form.cleaned_data[PASSWORD])
                user.save()
                sportsman = Sportsman()
                sportsman.phone_number = request.COOKIES.get(SIGN_UP_COOKIE_PHONE_NUMBER)
                sportsman.gender = request.COOKIES.get(SIGN_UP_COOKIE_GENDER)
                sportsman.birthday = datetime(
                    int(request.COOKIES.get(SIGN_UP_COOKIE_YEAR)),
                    int(request.COOKIES.get(SIGN_UP_COOKIE_MONTH)),
                    int(request.COOKIES.get(SIGN_UP_COOKIE_DAY))
                ).date()
                sportsman.avatar = "man.png" if request.COOKIES.get(SIGN_UP_COOKIE_GENDER) == "1" else "woman.png"
                sportsman.athlete = user
                sportsman.save()
                rating = Rating()
                rating.athlete = user
                rating.save()
                log_in(request, user)

                response = redirect("sportsmen-index")
                response.set_cookie(
                    SIGN_UP_PAGE,
                    SIGN_UP_PAGE_FIRST,
                    max_age=SIGN_UP_PAGE_COOKIE_AGE
                )
                return response
        return redirect("signup")


@require_http_methods(ONLY_GET)
def settings_email(request):
    response = redirect("sportsmen-index")
    if request.user.is_authenticated:
        sportsman = Sportsman.manager.get(pk=request.user.pk)
        sportsman.email_is_verified = True
        sportsman.save()
        response.set_cookie(
            SETTINGS_COOKIE_EMAIL_VERIFIED,
            IS_OK,
            max_age=SIGN_UP_PAGE_COOKIE_AGE
        )
    return response


@require_http_methods(GET_AND_POST)
def settings(request):
    if request.method == GET:
        user = request.user
        sportsman = Sportsman.manager.get(pk=user.pk)
        initial_context = {
            FIRST_NAME: user.first_name,
            LAST_NAME: user.last_name,
            GENDER: sportsman.gender,
            PHONE_NUMBER: sportsman.phone_number,
            EMAIL: user.email if sportsman.email_is_verified else "",
            AVATAR: sportsman.avatar
        }
        form = SettingsForm(initial=initial_context)
        has_error, error = request.COOKIES.get(SIGN_UP_COOKIE_ERROR, IS_OK), NONE
        if has_error == IS_NOT_OK:
            error = ugettext_lazy("Введенные данные некорректны")
        context = {
            FORM: form,
            AVATAR: sportsman.avatar,
            ERROR: error
        }
        response = render(request, "sportsmen/settings.html", context=context)
        response.set_cookie(
            SIGN_UP_COOKIE_ERROR,
            IS_OK,
            max_age=SIGN_UP_PAGE_COOKIE_AGE
        )
        return response
    elif request.method == POST:
        sportsman = Sportsman.manager.get(pk=request.user.pk)
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            response = redirect("sportsmen-index")
            sportsman.athlete.first_name = form.cleaned_data[FIRST_NAME]
            sportsman.athlete.last_name = form.cleaned_data[LAST_NAME]
            if sportsman.athlete.email != form.cleaned_data[EMAIL]:
                sportsman.email_is_verified = False
                sportsman.athlete.email = form.cleaned_data[EMAIL]
                send_celery_mail.delay(form.cleaned_data[EMAIL])
            sportsman.athlete.save()
            sportsman.phone_number = form.cleaned_data[PHONE_NUMBER]
            if form.cleaned_data[AVATAR]:
                sportsman.avatar = form.cleaned_data[AVATAR]
            sportsman.save()
            return response
        response = redirect("settings")
        response.set_cookie(
            SIGN_UP_COOKIE_ERROR,
            IS_NOT_OK,
            max_age=SIGN_UP_PAGE_COOKIE_AGE
        )
        return response


@require_http_methods(GET_AND_POST)
def achievements(request):
    if request.method == GET:
        has_error, error = request.COOKIES.get(SIGN_UP_COOKIE_ERROR, IS_OK), NONE
        if has_error == IS_NOT_OK:
            error = ugettext_lazy("Введенные данные некорректны")
        rating = Rating.manager.get(pk=request.user.pk)
        form = AchievementsForm(initial=rating.context())
        context = {
            FORM: form,
            ERROR: error
        }
        response = render(request, "sportsmen/achievements.html", context=context)
        response.set_cookie(
            SIGN_UP_COOKIE_ERROR,
            IS_OK,
            max_age=SIGN_UP_PAGE_COOKIE_AGE
        )
        return response
    elif request.method == POST:
        athlete = Rating.manager.get(pk=request.user.pk)
        form = AchievementsForm(request.POST, instance=athlete)
        if form.is_valid():
            form.save()
            return redirect("sportsmen-index")
        else:
            response = redirect("achievements")
            response.set_cookie(
                SIGN_UP_COOKIE_ERROR,
                IS_NOT_OK,
                max_age=SIGN_UP_PAGE_COOKIE_AGE
            )
            return response
