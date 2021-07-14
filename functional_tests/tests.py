#!/usr/bin/env python
# -*- coding: utf-8 -*-
# email: admin@jingwangnet.com
# author: jingwang
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

MAX_TIME = 3
QUESTION_PLACEHOLDER = 'Submit a question to vote!'
VOTE_PLACEHOLDER = 'Submit a vote for the question!'
FIRST_QUESTION = 'Where is the restarant for dinner?'
FIRST_VOTE = 'McDonald\'s is the best choice.'
SECOND_VOTE = 'I\'d like to KFC.'

SECOND_QUESTION = "I'd like to mall"
SECOND_QUESTION_VOTE = "I need new cloths"


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

    def check_element_not_in_the_page(self, method, string):
        '''method  is By.TAG_NAME or By.CLASS_NAME.....'''
        try:
            element = None
            element = self.browser.find_element(method, string)
        except NoSuchElementException:
            pass
        finally:
            self.assertIsNone(element)

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
        inputbox.send_keys(Keys.ENTER)
        # Joe see the question and vote
        self.wait_to_check_text_in_the_table('1. '+FIRST_VOTE, 'votes-table')
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
        inputbox.send_keys(SECOND_VOTE)
        inputbox.send_keys(Keys.ENTER)
        # Kim see the question and vote
        self.wait_to_check_text_in_the_table('2. '+SECOND_VOTE, 'votes-table')
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        # kim see the vote of joe
        self.wait_to_check_text_in_the_table('1. '+FIRST_VOTE, 'votes-table')

    def test_start_two_question_and_vote_each_other(self):
        # JoE visits the website
        self.browser.get(self.live_server_url)
        # there is inputbox to invite him to submit a question
        inputbox = self.browser.find_element(By.ID, 'new-question')
        # Joe submit a question
        inputbox.send_keys(FIRST_QUESTION)
        inputbox.send_keys(Keys.ENTER)
        # Joe saw the question 
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        # Joe get url of question
        FIRST_QUESTION_URL = self.browser.current_url
        # the question match pattern '/question/.+/'
        self.assertRegex(FIRST_QUESTION_URL, '/question/.+/')
        # there is no new-question inptbox
        # there is no questions-table inptbox
        # there is no vote-table inptbox
        self.check_element_not_in_the_page(By.ID, 'new-question')
        self.check_element_not_in_the_page(By.ID, 'questions-table')
        self.check_element_not_in_the_page(By.ID, 'votes-table')
        # there is a new inputbox to invite to subit a vote
        inputbox = self.browser.find_element(By.ID, 'new-vote')
        # he submit a vote 
        inputbox.send_keys(FIRST_VOTE)
        inputbox.send_keys(Keys.ENTER)
        # he saw the vote and question
        self.wait_to_check_text_in_the_table('1. '+FIRST_VOTE, 'votes-table')
        self.wait_to_check_text_in_the_page(FIRST_QUESTION)
        # Joe get url of vote 
        VOTE_OF_FIRST_QUESTION_URL = self.browser.current_url
        # the question match pattern '/question/.+/result/'
        self.assertRegex(VOTE_OF_FIRST_QUESTION_URL, '/question/.+/result/')
        # there is no new-question inptbox
        # there is no question-table inptbox
        # there is no new-vote inptbox
        self.check_element_not_in_the_page(By.ID, 'new-question')
        self.check_element_not_in_the_page(By.ID, 'questions-table')
        self.check_element_not_in_the_page(By.ID, 'new-vote')
        # he feels ok and leave
        self.browser.quit()
        # kim opens browser and visit the website too
        self.setUp()
        self.browser.get(self.live_server_url)
        # Kim saw the question of Joe
        self.wait_to_check_text_in_the_table('1. '+FIRST_QUESTION, 'question-table')
        # expect do not have vote of joe
        self.wait_to_check_text_in_the_page(FIRST_VOTE)
        # there is no new-vote inptbox
        # there is no votes-table
        self.check_element_not_in_the_page(By.ID, 'new-vote')
        self.check_element_not_in_the_page(By.ID, 'votes-table')
        # He submit a new question
        inputbox = self.browser.find_element(By.ID, 'new-question')
        inputbox.send_keys(SECOND_QUESTION)
        inputbox.send_keys(Keys.ENTER)
        # Kim saw the question , and Dont't except see the question of Joe
        self.wait_to_check_text_in_the_page(SECOND_QUESTION)
        html = self.browser.page_source
        self.assertNotIn(FIRST_VOTE, html)
        self.assertNotIn(FIRST_QUESTION, html)
        # Kim get url of question
        SECOND_QUESTION_URL = self.browser.current_url
        # the question match pattern '/question/.+/'
        self.assertRegex(SECOND_QUESTION_URL, '/question/.+/')
        # the url are not same the joes 
        self.assertNotEqual(
            FIRST_QUESTION_URL,
            SECOND_QUESTION_URL
        )
        # Kim return to the home_page, he see the quetion of self int the table
        self.browser.back()
        self.wait_to_check_text_in_the_table('2. '+SECOND_QUESTION, 'question-table')
        # kim return the url of qeustion
        SECOND_QUESTION_LINK = self.browser.find_element(By.PARTIAL_LINK_TEXT, SECOND_QUESTION)
        SECOND_QUESTION_LINK.click()
        time.sleep(1)
        # Kim submit a vote 
        inputbox = self.browser.find_element(By.ID, 'new-vote')
        inputbox.send_keys(SECOND_QUESTION_VOTE)
        inputbox.send_keys(Keys.ENTER)
        # Kim saw the vote and the question
        self.wait_to_check_text_in_the_table('1. '+SECOND_QUESTION_VOTE, 'votes-table')
        self.wait_to_check_text_in_the_page(SECOND_QUESTION)
        # the question match pattern '/question/.+/result/'
        VOTE_OF_SECOND_QUESTION = self.browser.current_url
        self.assertRegex(VOTE_OF_SECOND_QUESTION, '/question/.+/result/')
        # He dont't expect see the vote of joe
        # the page not have new-vote inputb
        html = self.browser.page_source
        self.assertNotIn(FIRST_VOTE, html)
        self.assertNotIn(FIRST_QUESTION, html)
