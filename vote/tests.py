from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from vote.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_used_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'vote/index.html')

    def test_home_page_can_save_new_question_post_request(self):
        response = self.client.post('/', data={'new-question': 'A new question'})
        self.assertContains(response, 'A new question')
        self.assertTemplateUsed(response, 'vote/index.html')

    def test_home_page_can_save_new_post_post_request(self):
        response = self.client.post('/', data={'new-vote': 'A new vote'})
        self.assertContains(response, 'A new vote')
        self.assertTemplateUsed(response, 'vote/index.html')

