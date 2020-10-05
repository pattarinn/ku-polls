"""Module for managing admin page."""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """A class for giving the amount of initialize choices in UI."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """A class for displaying questions in database."""

    list_display = ('question_text', 'pub_date', 'was_published_recently', 'end_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
