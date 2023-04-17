from django.contrib import admin

from .models import Road, Report, Rating, Suggestion, City


class ReportInline(admin.StackedInline):
    model = Report
    extra = 0


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 0


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = ('name', 'status',)
    list_filter = ('status',)
    inlines = [ReportInline, RatingInline]


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('username', 'text', 'photo')
    pass


@admin.register(Rating)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('username', 'road', 'rate', 'comment')
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('username', 'date', 'road', 'photo', 'text')
    pass
