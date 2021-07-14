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
import time

MAX_TIME = 3
QUESTION_PLACEHOLDER = 'Submit a question to vote!'
VOTE_PLACEHOLDER = 'Submit a vote for the question!'
FIRST_QUESTION = 'Where is the restarant for dinner?'
FIRST_VOTE = 'McDonald\'s is the best choice.'
SECOND_VOTE = 'I\'d like to KFC.'


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def wait_to_check_text_in_the_table(self, text, table_id):
        START_TIME = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, table_id)
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(
                    text, 
                    [row.text for row in rows]
                )
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - START_TIME > MAX_TIME:
                    raise e
                time.sleep(0.5)

    def wait_to_check_text_in_the_page(self, text):
        START_TIME = time.time()
        while True:
            try:
                html = self.browser.find_element(By.TAG_NAME, 'body').text
                self.assertIn(text, html)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - START_TIME > MAX_TIME:
                    raise e
                time.sleep(0.5)
        


    def test_submit_a_question_and_votes_it_twice(self):
        # Joe visits the website
        self.browser.get(self.live_server_url)
        # there are 'Voting For Your Question'  at the title and header
        self.assertIn('Voting For Your Question', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Voting For Your Question', header_text)
        # there is inputbox to invite him to submit a question
        inputbox = self.browser.find_element(By.ID, 'new-question')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            QUESTION_PLACEHOLDER
        )
        # Joe submit a question
        inputbox.send_keys(FIRST_QUESTION)
        inputbox.send_keys(Keys.ENTER)
        # Joe see the question, 
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        # and he see a new inputbox to invite him to submit a vote
        inputbox = self.browser.find_element(By.ID, 'new-vote')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            VOTE_PLACEHOLDER
            
        )
        # Joe submit a vote agian
        inputbox.send_keys(FIRST_VOTE)
        inputbox.send_keys(keys.ENTER)
        # Joe see the question and vote
        self.wait_to_check_text_in_the_table('1. '+FIRST_VOTEE, 'votes-table')
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        # He feels good and leave
        self.browser.quit()
        self.setUp()
        # Kim visit the website,
        self.browser.get(self.live_server_url)
        # Kim see the question of Joe, he click the question 
        self.wait_to_check_text_in_the_table('1. '+FIRST_QUESTION, 'questions-table')
        FIRST_QUESTION_LINK = self.browser.find_element(By.PARTIAL_LINK_TEXT, FIRST_QUESTION)
        FIRST_QUESTION_LINK.click()
        time.sleep(0.3)
        # Kim see the question and vote of Joe
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        inputbox = self.browser.find_element(By.ID, 'new-vote')
        # Kim vote agian 
        inputbox.send_keys(FIRST_VOTE)
        inputbox.send_keys(keys.ENTER)
        # Kim see the question and vote
        self.wait_to_check_text_in_the_table('2. '+SECOND_VOTEE, 'votes-table')
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        # kim see the vote of joe
        self.wait_to_check_text_in_the_table('1. '+FIRST_VOTEE, 'votes-table')
        





  

