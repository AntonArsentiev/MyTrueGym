from .views import *
from django.urls import path


urlpatterns = [
    path("account/settings/email", settings_email, name="settings-email"),
    path("account/signup/", signup, name="signup"),
    path("account/login/", login, name="login"),
    path("account/logout/", logout, name="logout"),
    path("account/settings/", settings, name="settings"),
    path("account/achievements/", achievements, name="achievements"),
    path("account/", sportsmen_info, name="sportsmen-info"),
    path("account/lang/<slug:lang>/", sportsmen_lang, name="sportsmen-lang"),
    path("", index, name="sportsmen-index"),
]
