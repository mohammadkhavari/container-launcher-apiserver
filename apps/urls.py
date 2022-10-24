from django.urls import path
from apps.views import AppList, AppDetail

urlpatterns = [
    path('', AppList.as_view()),
    path('<int:pk>/', AppDetail.as_view()),
]
