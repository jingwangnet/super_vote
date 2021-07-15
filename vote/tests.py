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

    def test_display_all_questions(self):
        Question.objects.create(text='A new question')
        Question.objects.create(text='A new question agian')
        response = self.client.get('/')
        self.assertContains(response, 'A new question')
        self.assertContains(response, 'A new question agian')

class NewQuestionTest(TestCase):
    def test_can_save_new_question_post_request(self):
        response = self.client.post('/question/new', data={'new-question': 'A new question'})

        self.assertEqual(1, Question.objects.count())
        question = Question.objects.first()
        self.assertEqual(question.text, 'A new question')

    def test_redirect_after_save_new_question_post_request(self):
        response = self.client.post('/question/new', data={'new-question': 'A new question'})
        question = Question.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/question/{question.pk}/')

class ViewQuestionTest(TestCase):
    def test_display_question_for_special(self):
        other_question = Question.objects.create(text='other question')
        correct_question = Question.objects.create(text='correct question')
        response = self.client.get(f'/question/{correct_question.pk}/')
        self.assertContains(response, 'correct question')

    def test_use_template(self):
        question=Question.objects.create(text='A new question')
        response = self.client.get(f'/question/{question.pk}/')
        self.assertTemplateUsed(response, 'vote/question.html')

class NewVoteTest(TestCase):
    def test_can_save_new_vote_post_request(self):
        question=Question.objects.create(text='A new question')
        response = self.client.post(f'/question/{question.pk}/new', data={'new-vote': 'A new vote'})

        self.assertEqual(1, Vote.objects.count())
        vote = Vote.objects.first()
        self.assertEqual(vote.text, 'A new vote')

    def test_redirect_after_save_new_vote_post_request(self):
        question=Question.objects.create(text='A new question')
        response = self.client.post(f'/question/{question.pk}/new', data={'new-vote': 'A new vote'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/question/{question.pk}/result/')

class ViewVoteTest(TestCase):
    def test_display_all_votes(self):
        question=Question.objects.create(text='A new question')
        Vote.objects.create(text='A new vote', question=question)
        Vote.objects.create(text='A new vote agian', question=question)
        response = self.client.get(f'/question/{question.pk}/result/')
        self.assertContains(response, 'A new vote')
        self.assertContains(response, 'A new vote agian')

    def test_use_template(self):
        question=Question.objects.create(text='A new question')
        Vote.objects.create(text='A new vote', question=question)
        response = self.client.get(f'/question/{question.pk}/result/')
        self.assertTemplateUsed(response, 'vote/vote.html')

class QuestionModelTest(TestCase):

    
    def test_create_a_question_and_retrieve_it_later(self):
        question = Question()
        question.text = 'the question'
        question.save()

        self.assertEqual(1, Question.objects.count())
        saved_question = Question.objects.first()
        self.assertEqual(saved_question.text, 'the question')

    def test_question_url(self):
        question = Question()
        question.text = 'the question'
        question.save()

        self.assertEqual('/question/1/', question.get_absolute_url())

          
    def test_create_two_votes_and_retrieve_them_later(self):
        question = Question()
        question.text = 'the question'
        question.save()
        first_vote = Vote.objects.create(text="the first vote", question=question)
        second_vote = Vote.objects.create(text="the second vote", question=question)
        self.assertEqual(2, Vote.objects.count())
        first_saved_vote = Vote.objects.all()[0]
        second_saved_vote = Vote.objects.all()[1]
        self.assertEqual(first_saved_vote.text, 'the first vote')
        self.assertEqual(second_saved_vote.text, 'the second vote')
