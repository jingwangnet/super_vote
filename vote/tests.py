from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from vote.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_used_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'vote/index.html')


        






