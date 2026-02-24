from django.urls import path
from .views import scheme_list, recommend_schemes

urlpatterns = [
    path('schemes/', scheme_list),
    path('recommend/', recommend_schemes),
]
