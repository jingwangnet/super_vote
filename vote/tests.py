from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from vote.views import home_page
from vote.models import Question, Vote

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_used_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'vote/index.html')

    def test_home_page_can_save_new_question_post_request(self):
        response = self.client.post('/', data={'new-question': 'A new question'})

        self.assertEqual(1, Question.objects.count())
        question = Question.objects.first()
        self.assertEqual(question.text, 'A new question')

    def test_redirect_after_save_new_question_post_request(self):
        response = self.client.post('/', data={'new-question': 'A new question'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_display_question(self):
        Question.objects.create(text='A new question')
        response = self.client.get('/')
        self.assertContains(response, 'A new question')

    def test_home_page_can_save_new_vote_post_request(self):
        response = self.client.post('/', data={'new-vote': 'A new vote'})

        self.assertEqual(1, Vote.objects.count())
        vote = Vote.objects.first()
        self.assertEqual(vote.text, 'A new vote')

    def test_redirect_after_save_new_vote_post_request(self):
        response = self.client.post('/', data={'new-vote': 'A new vote'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_display_all_votes(self):
        first_vote = Vote.objects.create(text='The first vote')
        second_vote = Vote.objects.create(text='The second vote')
        response = self.client.get('/')
        self.assertContains(response, 'The first vote')
        self.assertContains(response, 'The second vote')



class QuestionModelTest(TestCase):

    
    def test_create_a_question_and_retrieve_it_later(self):
        question = Question()
        question.text = 'the question'
        question.save()

        self.assertEqual(1, Question.objects.count())
        saved_question = Question.objects.first()
        self.assertEqual(saved_question.text, 'the question')

    def test_create_two_votes_and_retrieve_them_later(self):
        first_vote = Vote()
        first_vote.text = "the first vote"
        first_vote.save()
        second_vote = Vote()
        second_vote.text = "the second vote"
        second_vote.save()
        self.assertEqual(2, Vote.objects.count())
        first_saved_vote = Vote.objects.all()[0]
        second_saved_vote = Vote.objects.all()[1]
        self.assertEqual(first_saved_vote.text, 'the first vote')
        self.assertEqual(second_saved_vote.text, 'the second vote')
