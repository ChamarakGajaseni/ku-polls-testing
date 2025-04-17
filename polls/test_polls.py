import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from .models import Question, Choice, Vote
import datetime

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    # Delete any existing test user to avoid unique constraint issues
    User.objects.filter(username='testuser').delete()
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.fixture
def question():
    # Create a new question for each test
    return Question.objects.create(
        question_text="Test Question",
        pub_date=timezone.now() - datetime.timedelta(days=1)
    )

@pytest.fixture
def choice(question):
    return Choice.objects.create(
        question=question,
        choice_text="Test Choice"
    )

@pytest.mark.django_db
class TestQuestionModel:

    def test_is_published(self, question):
        assert question.is_published() is True

    def test_can_vote_without_end_date(self, question):
        assert question.can_vote() is True

    def test_can_vote_with_end_date(self):
        # Create a new question for this specific test
        question = Question.objects.create(
            question_text="Test Question with End Date",
            pub_date=timezone.now() - datetime.timedelta(days=1),
            end_date=timezone.now() + datetime.timedelta(days=1)
        )
        assert question.can_vote() is True

    def test_cannot_vote_after_end_date(self):
        # Create a new question for this specific test
        question = Question.objects.create(
            question_text="Test Question Past End Date",
            pub_date=timezone.now() - datetime.timedelta(days=2),
            end_date=timezone.now() - datetime.timedelta(days=1)
        )
        assert question.can_vote() is False

@pytest.mark.django_db
class TestChoiceModel:
    def test_choice_votes(self, choice, user):
        Vote.objects.create(user=user, choice=choice)
        assert choice.votes == 1

    def test_choice_str(self, choice):
        assert str(choice) == "Test Choice"

@pytest.mark.django_db
class TestVoteModel:
    def test_vote_creation(self, choice, user):
        vote = Vote.objects.create(user=user, choice=choice)
        assert str(vote) == f"{user.username} voted for {choice.choice_text}"

@pytest.mark.django_db
class TestViews:
    def test_index_view(self, client, question):
        response = client.get(reverse('polls:index'))
        assert response.status_code == 200
        assert question.question_text in str(response.content)

    def test_detail_view(self, client, question):
        response = client.get(reverse('polls:detail', args=(question.id,)))
        assert response.status_code == 200
        assert question.question_text in str(response.content)

    def test_results_view(self, client, question):
        response = client.get(reverse('polls:results', args=(question.id,)))
        assert response.status_code == 200
        assert question.question_text in str(response.content)

    def test_vote_view_requires_login(self, client, question, choice):
        response = client.post(reverse('polls:vote', args=(question.id,)), {'choice': choice.id})
        assert response.status_code == 302  # Redirects to login page

    def test_vote_view_with_login(self, client, user, question, choice):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('polls:vote', args=(question.id,)), {'choice': choice.id})
        assert response.status_code == 302  # Redirects to results page
        assert Vote.objects.filter(user=user, choice=choice).exists()

    def test_create_poll_view_requires_login(self, client):
        response = client.get(reverse('polls:create'))
        assert response.status_code == 302  # Redirects to login page

    def test_create_poll_view_with_login(self, client, user):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('polls:create'))
        assert response.status_code == 200

    def test_create_poll_post(self, client, user):
        client.login(username='testuser', password='testpass123')
        response = client.post(reverse('polls:create'), {
            'question_text': 'New Question',
            'choice_set-TOTAL_FORMS': '2',
            'choice_set-0-choice_text': 'Choice 1',
            'choice_set-1-choice_text': 'Choice 2'
        })
        assert response.status_code == 302  # Redirects to detail page
        assert Question.objects.filter(question_text='New Question').exists()
        assert Choice.objects.filter(choice_text='Choice 1').exists()
        assert Choice.objects.filter(choice_text='Choice 2').exists() 