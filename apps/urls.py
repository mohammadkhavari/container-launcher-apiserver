from django.urls import path, include
from apps.views import AppViewSet, RunList
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'apps', AppViewSet, basename="apps")

urlpatterns = [
    path('', include(router.urls)),
    path('apps/<int:pk>/run', RunList.as_view())
]
