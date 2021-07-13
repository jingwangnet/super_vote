from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from vote.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_can_resolve_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_can_return_correct_content(self):
        request = HttpRequest()
        response = home_page(request)

        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Voting For Your Question</title>', html)
        #self.fail(repr(html))
        self.assertTrue(html.strip().endswith('</html>'))




