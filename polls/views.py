from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Choice, Question, Vote
import logging
from django.http import Http404
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter()

    def get(self, request, *args, **kwargs):
        """
        Check if Question is pending using self.object.can_vote().
        If voting is not allowed, we set an error.
        Then, we redirect the user to the polls index page.
        """
        self.object = self.get_object()
        if not self.object.can_vote():
            messages.error(request, "Voting is not allowed for this question.")
            return redirect('polls:index')
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


logger = logging.getLogger('polls')


@login_required
def vote(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    try:
        question = Question.objects.get(pk=question_id)

    except Question.DoesNotExist:
        logger.error(f"Question with id: {question_id} not found")
        raise Http404("Question not found.")

    user = request.user

    # Ensure the question is open for voting
    if not question.can_vote():
        logger.warning
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "The Question is not pending currently.",
        })

    # Check if the user has already voted for this question
    user_vote = Vote.objects.filter(user=user,
                                    choice__question=question).last()

    if request.method == 'POST':
        # Handle the vote submission
        try:
            selected_choice = question.choice_set.get(
                pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form if no choice was selected
            logger.warning("Invalid question id or didn't selected choice")
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
                'user_vote': user_vote  # Show the user's previous vote
            })

        # If the user has already voted,
        # delete the old vote before saving the new one
        if user_vote:
            if user_vote.choice == selected_choice:
                messages.info(request, f"You already voted for"
                              f"'{user_vote.choice.choice_text}'.")
            else:
                user_vote.delete()
                messages.info(request, f"Your previous vote for"
                              f"'{user_vote.choice.choice_text}'"
                              f"has been removed.")

                # Create a new vote for the selected choice
                Vote.objects.create(user=user, choice=selected_choice)
                messages.success(request,
                                 f"Your vote '{selected_choice.choice_text}'"
                                 f"was recorded.")
        else:
            Vote.objects.create(user=user, choice=selected_choice)
            messages.success(request, f"Your vote "
                             f"'{selected_choice.choice_text}'"
                             f"was recorded.")

        logger.info("Vote submitted for poll #{0}".format(question_id))
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))

    # If it's a GET request, show the question and the user's previous vote
    return render(request, 'polls/detail.html', {
        'question': question,
        'user_vote': user_vote  # Show the user's previous vote
    })


def get_client_ip(request):
    """Get the visitor's IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)  # Fetch the user's IP address
    logger.info(f"User {user.username} logged in from {ip_addr}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)  # Fetch the user's IP address
    logger.info(f"User {user.username} logged out from {ip_addr}")


@login_required
def create_poll(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if not question_text:
            messages.error(request, 'Question text is required.')
            return redirect('polls:create')
            
        question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now()
        )
        
        # Process choices
        total_forms = int(request.POST.get('choice_set-TOTAL_FORMS', 0))
        for i in range(total_forms):
            choice_text = request.POST.get(f'choice_set-{i}-choice_text')
            if choice_text:
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text
                )
        
        messages.success(request, 'Poll created successfully.')
        return redirect('polls:detail', pk=question.id)
        
    return render(request, 'polls/create.html')
