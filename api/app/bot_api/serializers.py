from rest_framework import serializers
from .models import Report, Suggestion, Rating, Road, City
import base64  # Модуль с функциями кодирования и декодирования base64

from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    roads = RoadSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ('pk', 'name', 'roads')


class ReportSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Report
        fields = ('username', 'road', 'text', 'photo')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class SuggestionSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Suggestion
        fields = '__all__'