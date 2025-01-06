# blocks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FirstPageViewSet, SecondPageViewSet, ThirdPageViewSet

router = DefaultRouter()

# Регистрируем маршруты для каждой страницы отдельно
router.register('first-page', FirstPageViewSet, basename='first-page')
router.register('second-page', SecondPageViewSet, basename='second-page')
router.register('third-page', ThirdPageViewSet, basename='third-page')

urlpatterns = [
    path('', include(router.urls)),
]