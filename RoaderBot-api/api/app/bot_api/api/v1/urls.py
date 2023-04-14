from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, RatingViewSet, SuggestionViewSet, CityViewSet

router = DefaultRouter()
router.register('reports', ReportViewSet)
router.register('ratings', RatingViewSet)
router.register('suggestions', SuggestionViewSet)
router.register('cities', CityViewSet)

urlpatterns = [
    path('', include(router.urls))
]