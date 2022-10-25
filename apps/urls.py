from django.urls import path
from apps.views import AppList, AppDetail, RunList

urlpatterns = [
    path('', AppList.as_view()),
    path('<int:pk>/', AppDetail.as_view()),
    path('<int:pk>/run', RunList.as_view())
]
