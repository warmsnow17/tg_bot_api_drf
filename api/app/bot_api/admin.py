from django.contrib import admin

from .models import Road, Report, Rating, Suggestion


class ReportInline(admin.StackedInline):
    model = Report
    extra = 0


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 0


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', )
    list_filter = ('status', )
    inlines = [ReportInline, RatingInline]


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    pass
