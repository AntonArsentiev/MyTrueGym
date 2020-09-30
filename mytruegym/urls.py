from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler404, handler500, handler403


urlpatterns = [
    path("", include("sportsmen.urls")),
    path("calories/", include("calories.urls")),
    path("ratings/", include("ratings.urls")),
    path("admin/", admin.site.urls)
]


handler400 = "sportsmen.views.page_400"
handler403 = "sportsmen.views.page_403"
handler404 = "sportsmen.views.page_404"
handler500 = "sportsmen.views.page_500"
