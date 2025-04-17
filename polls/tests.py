import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question, User, Choice, Vote
from django.urls import reverse
import pytest
from django.test import Client
from django.contrib.auth.models import User

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(
            list(response.context['latest_question_list']),
            [question],
            )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
    def is_published_with_future_pub_date(self):
        """
        is_published should be false,
        if question is set to be published in the future.
        """
        future_pub_date = timezone.now() +timezone.timedelta(days=1)
        question = Question(pubdate=future_pub_date)
        self.assertIs(question.is_published(),False)
        
    def is_published_with_past_pub_date(self):
        """
        is_published should be True,
        if question was published in the past.
        """
        past_pub_date = timezone.now() - timezone.timedelta(days=1)
        question = Question(pubdate=past_pub_date)
        self.assertIs(question.is_published(),True)
        
    def is_published_now(self):
        """
        is_published should be True,
        if question is published now.
        """
        question = Question(pubdate=timezone.now())
        self.assertIs(question.is_published(),True)
    
    def test_cannot_vote_after_end_date(self):
        """
        Cannot vote if current time is passed end_date.
        """
        past_pub_date = timezone.now() - timezone.timedelta(days=1)
        question = Question(pub_date=timezone.now(), end_date=past_pub_date)
        self.assertIs(question.can_vote(), False)

    def test_cannot_vote_before_pub_date(self):
        """
        Cannot vote if current time is passed end_date.
        """
        future_pub_date = timezone.now() + timezone.timedelta(days=1)
        question = Question(pub_date=future_pub_date, end_date= future_pub_date + timezone.timedelta(days=10))
        self.assertIs(question.can_vote(), False)
        
    def test_can_vote_published_now(self):
        """
        Can vote if question pub_date is equals to the time now
        """
        question = Question(pub_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=1) )
        self.assertIs(question.can_vote(), True)

    def test_can_vote_during_pending_time(self):
        """
        Can vote if current time is between pub_date and end_date.
        """
        past_pub_date = timezone.now() - timezone.timedelta(days=1)
        future_end_date = timezone.now() + timezone.timedelta(days=1)
        question = Question(pub_date=past_pub_date,end_date=future_end_date)
        self.assertIs(question.can_vote(), True)
        
class QuestionDetailViewTests(TestCase):

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    
    def test_future_question(self):
        """
        Cannot see question's detail if it isn't published yet. 
        """
        future_question = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertRedirects(response, reverse('polls:index'))

class VoteViewTests(TestCase):
    """Test the voting view for the KU Polls application."""

    def setUp(self):
        """Set up the initial data for the tests."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.question = create_question(question_text="Sample Question", days=-1)
        self.choice = Choice.objects.create(question=self.question, choice_text="Choice 1")

    def test_vote_success(self):
        """Test that a valid vote is recorded and redirected to results."""
        self.client.login(username='testuser', password='12345')
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.post(url, {'choice': self.choice.id})
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().choice, self.choice)

    def test_vote_after_end_date(self):
        """Attempting to vote after the question's end_date should fail."""
        past_question = create_question(question_text="Past Question", days=-10)
        past_question.end_date = timezone.now() - timezone.timedelta(days=1)
        past_question.save()
        url = reverse('polls:vote', args=(past_question.id,))
        self.client.login(username='testuser', password='12345')

        with self.assertLogs('polls', level='WARNING') as log:
            response = self.client.post(url, {'choice': self.choice.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This poll is not allowed for voting.")
        self.assertTrue(any(f"User testuser tried to vote on a closed poll {past_question.id}" in message for message in log.output))

    def test_user_cannot_vote_multiple_times(self):
        """A user should not be able to vote multiple times for the same question."""
        self.client.login(username='testuser', password='12345')
        url = reverse('polls:vote', args=(self.question.id,))
        self.client.post(url, {'choice': self.choice.id})
        response = self.client.post(url, {'choice': self.choice.id})
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(Vote.objects.count(), 1)  # User should only have one vote for this question

    def test_vote_missing_choice(self):
        """Test that a missing choice triggers an error and logs it."""

        self.client.login(username='testuser', password='12345')
        url = reverse('polls:vote', args=(self.question.id,))

        # Capture the logs during the request
        with self.assertLogs('polls', level='WARNING') as log:
            response = self.client.post(url, {})  # Empty POST data (no choice selected)

        # Assert that the correct error message was shown
        self.assertEqual(response.status_code, 200)

        # Assert that the log contains the expected warning message
        self.assertTrue(any("Choice ID not found in POST data" in message for message in log.output))
        
@pytest.mark.django_db
class TestPollCreation:
    def test_create_poll(self, client):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='12345')
        client.force_login(user)
        
        # Create a test poll
        response = client.post(reverse('polls:create'), {
            'question_text': 'Test Question',
            'choice_set-TOTAL_FORMS': '2',
            'choice_set-INITIAL_FORMS': '0',
            'choice_set-MIN_NUM_FORMS': '0',
            'choice_set-MAX_NUM_FORMS': '1000',
            'choice_set-0-choice_text': 'Choice 1',
            'choice_set-1-choice_text': 'Choice 2',
        })
        
        assert response.status_code == 302  # Redirect after successful creation
        assert Question.objects.count() == 1
        assert Choice.objects.count() == 2

@pytest.mark.django_db
class TestPollVoting:
    def test_vote_on_poll(self, client):
        # Create test data
        user = User.objects.create_user(username='testuser', password='12345')
        client.force_login(user)
        
        question = Question.objects.create(question_text='Test Question')
        choice = Choice.objects.create(question=question, choice_text='Test Choice')
        
        # Vote on the poll
        response = client.post(reverse('polls:vote', args=(question.id,)), {
            'choice': choice.id
        })
        
        assert response.status_code == 302  # Redirect after successful vote
        assert Vote.objects.filter(choice=choice).count() == 1

@pytest.mark.django_db
class TestPollResults:
    def test_view_results(self, client):
        # Create test data
        question = Question.objects.create(question_text='Test Question')
        choice1 = Choice.objects.create(question=question, choice_text='Choice 1')
        choice2 = Choice.objects.create(question=question, choice_text='Choice 2')
        
        # Add some votes
        user1 = User.objects.create_user(username='user1', password='12345')
        user2 = User.objects.create_user(username='user2', password='12345')
        user3 = User.objects.create_user(username='user3', password='12345')
        
        Vote.objects.create(user=user1, choice=choice1)
        Vote.objects.create(user=user2, choice=choice1)
        Vote.objects.create(user=user3, choice=choice1)
        
        Vote.objects.create(user=user1, choice=choice2)
        Vote.objects.create(user=user2, choice=choice2)
        
        # View results
        response = client.get(reverse('polls:results', args=(question.id,)))
        
        assert response.status_code == 200
        assert 'Test Question' in str(response.content)
        assert 'Choice 1' in str(response.content)
        assert 'Choice 2' in str(response.content)

@pytest.mark.django_db
class TestUserAuthentication:
    def test_user_login(self, client):
        # Create a test user
        User.objects.create_user(username='testuser', password='12345')
        
        # Attempt login
        response = client.post(reverse('polls:login'), {
            'username': 'testuser',
            'password': '12345'
        })
        
        assert response.status_code == 302  # Redirect after successful login
        
    def test_user_logout(self, client):
        # Create and login a test user
        user = User.objects.create_user(username='testuser', password='12345')
        client.force_login(user)
        
        # Attempt logout
        response = client.post(reverse('polls:logout'))
        
        assert response.status_code == 302  # Redirect after successful logout
