"""Module for testing question model test."""
import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    """A test class for checking models."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_at_day_before_published(self):
        """is_published returns False if the day is before pub_date."""
        time = timezone.now() + datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(recent_question.is_published(), False)

    def test_is_published_at_day_after_published(self):
        """is_published returns True if the day is after pub_date."""
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote_before_published(self):
        """can_vote returns False if it can't be voted (the question is not published)."""
        time = timezone.now() + datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(recent_question.can_vote(), False)

    def test_can_vote_after_published(self):
        """can_vote returns True if it can't be voted (the question is not published)."""
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=31))
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_after_end_date(self):
        """can_vote returns False if it can't be voted (the question is not in the polling period)."""
        time = timezone.now()
        recent_question = Question(pub_date=time, end_date=timezone.now() - datetime.timedelta(days=31))
        self.assertIs(recent_question.can_vote(), False)