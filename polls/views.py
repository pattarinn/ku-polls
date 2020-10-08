"""Controlling the flow of the application."""

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Question, Choice


class IndexView(generic.ListView):
    """A class for creating index page."""

    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """
        Get polls that are in polling period.

        Returns:
             Polls that are in polling period.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """A class for creating detail view page."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.

        Returns:
            Polls that are published.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """A class for creating result page."""

    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Vote a choice in the poll.

    Arguments:
        request: user's request
        question_id: the id of question that user requested.

    Returns:
        Detail page if the choice is not selected. Else, the result page of that question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def can_access(request, question_id):
    """
    can_access checks if the question is in polling period.

    If it is in the polling period, visitors will be able to access to detail page.
    If it isn't, visitors will be redirected to poll index page with the error message.

    Arguments:
        request: user's request
        question_id: the id of question that user requested.

    Returns:
        Poll index page if the requested question is not in the polling period.

    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, f"The question is not in the polling period.")
        return redirect('polls:index')
    else:
        return vote(request, question_id)
