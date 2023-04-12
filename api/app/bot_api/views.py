from rest_framework import mixins, viewsets
from .models import Rating, Report, Suggestion
from .serializers import (RatingSerializer,
                          ReportSerializer,
                          SuggestionSerializer)


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class ReportViewSet(CreateViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class RatingViewSet(CreateViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class SuggestionViewSet(CreateViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer