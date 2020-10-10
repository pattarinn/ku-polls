"""Module for creating question and choice in database."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """A class for making a question in database."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        was_published_recently checks if the question is published within 1 day.

        Returns:
            bool: True if the time is less than 1 day, otherwise, False.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """
        Check if the question is published.

        Returns:
            bool: True if the question is published, otherwise, False.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        Check if the question can be voted now.

        Returns:
            bool: True if the question can be voted for now, else, False.
        """
        now = timezone.now()
        return self.is_published() and now <= self.end_date


class Choice(models.Model):
    """A class for making a choice in database."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
