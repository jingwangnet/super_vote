#!/usr/bin/env python
# -*- coding: utf-8 -*-
# email: admin@jingwangnet.com
# author: jingwang
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_submit_a_question_and_votes_it_twice(self):
        # Joe visits the website
        self.browser.get(self.live_server_url)
        # there are 'Voting For Your Question'  at the title and header
        self.assertIn('Voting For Your Question', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Voting For Your Question', header_text)
        # there is inputbox to invite him to submit a question
        # Joe submit a question
        # Joe see the question, 
        # and he see a new inputbox to invite him to submit a vote
        # Joe submit a vote agian
        # Joe see the question and vote
        # He feels good and leave
        # Kim visit the website,
        # Kim see the question of Joe, he click the question 
        # There is a inputbox to invite him to submit a vote
        # Kim vote 
        # Kim see the question and vote
        # kim see the vote of joe
        





  

