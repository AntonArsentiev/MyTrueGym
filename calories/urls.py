from django.urls import path
from .views import index, find_by_query


urlpatterns = [
    path("find/<str:query>/", find_by_query, name="calories-find"),
    path("", index, name="calories-index")
]
