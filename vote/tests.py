from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from vote.views import home_page
from vote.models import Question

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

    def test_display_all_question(self):
        Question.objects.create(text='A new question')
        response = self.client.get('/')
        self.assertContains(response, 'A new question')

    def test_home_page_can_save_new_vote_post_request(self):
        response = self.client.post('/', data={'new-vote': 'A new vote'})
        self.assertContains(response, 'A new vote')
        self.assertTemplateUsed(response, 'vote/index.html')


class QuestionModelTest(TestCase):

    
    def test_create_a_question_and_retrieve_it_later(self):
        question = Question()
        question.text = 'the question'
        question.save()

        self.assertEqual(1, Question.objects.count())
        saved_question = Question.objects.first()
        self.assertEqual(saved_question.text, 'the question')

