from rest_framework import mixins, viewsets
from bot_api.models import Rating, Report, Suggestion, Road, City
from bot_api.serializers import (RatingSerializer,
                                 ReportSerializer,
                                 SuggestionSerializer,
                                 RoadSerializer,
                                 CitySerializer)


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RoadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer


class ReportViewSet(CreateViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class RatingViewSet(CreateViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class SuggestionViewSet(CreateViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer