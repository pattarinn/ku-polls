"""Controlling the flow of the application."""
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed, authenticate, login
from .models import Question, Choice, Vote
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# class IndexView(generic.ListView):
#     """A class for creating index page."""
#
#     template_name = 'polls/index.html'
#     context_object_name = 'question_list'
#
#     def get_queryset(self):
#         """
#         Get polls that are in polling period.
#
#         Returns:
#              Polls that are in polling period.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


def index_view(request):
    """
    Creating index page

    Arguments:
        request: user's request

    Return:
        Polls index page

    """
    context = {'question_list': Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
               }
    return render(request, 'polls/index.html', context)


# class DetailView(generic.DetailView):
#     """A class for creating detail view page."""
#     model = Question
#     template_name = "polls/detail.html"
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#
#         Returns:
#             Polls that are published.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())

def detail_view(request, pk):
    """
    Creating detail page

    Arguments:
        request: user's request
        pk: id of question to look for

    Return:
        Polls detail page
    """
    question = Question.objects.get(pk=pk)
    try:
        if question.can_vote():
            vote_choice = Vote.objects.filter(user_id=request.user.id, question_id=question.id).exists()
            if vote_choice:
                vote_choice = Vote.objects.get(user_id=request.user.id, question_id=question.id)
                context = {'question': question, 'voted_choice': vote_choice.choice_id}
            else:
                context = {'question': question, 'voted_choice': None}
            return render(request, "polls/detail.html", context)
        else:
            raise Http404("This question is not in the polling period")
    except Http404:
        messages.error(request, f"The question is not in the polling period.")
        return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """A class for creating result page."""

    model = Question
    template_name = "polls/results.html"


# def result_view(request):
#     # context = {}
#     return render(request, "polls/results.html")


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
        # selected_choice.votes += 1
        # selected_choice.save()
        # logger.info(f"{request.user.username} voted on question id: {question.id}")
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # user = request.user
        # try:
        #     user.vote_set.get(pk=request.POST['choice'])
        # except (KeyError, Choice.DoesNotExist):
        #     user.vote_set.add(request.POST['choice'])
        # finally:
        #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        user_id = request.user.id
        try:
            vote_choice = Vote.objects.get(user_id=user_id, question_id=question_id)
            vote_choice.choice_id = selected_choice.id
            vote_choice.save()
        except Vote.DoesNotExist:
            vote_choice = Vote.objects.create(user_id=user_id, choice_id=selected_choice.id, question_id=question_id)
            vote_choice.save()
        finally:
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


@receiver(user_logged_out)
def user_logout(request, **kwargs):
    logger.info(f"{request.user.username} logged out, IP: {request.META.get('REMOTE_ADDR')}")


@receiver(user_logged_in)
def user_login(request, **kwargs):
    logger.info(f"{request.user.username} logged in, IP: {request.META.get('REMOTE_ADDR')}")


@receiver(user_login_failed)
def user_login(request, **kwargs):
    username = request.POST['username']
    logger.warning(f"warning: {username} logged in failed, IP: {request.META.get('REMOTE_ADDR')}")

# def user_login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         logger.info(f"{request.user.username} logged in, IP: {request.META.get('REMOTE_ADDR')}")
#         login(request, user)
#         # return redirect('polls:index')
#     else:
#         logger.warning(f"warning: {username} logged in failed, IP: {request.META.get('REMOTE_ADDR')}")
#     context = {}
#     return render(request, 'polls/login.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

