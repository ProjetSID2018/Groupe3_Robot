#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:19:52 2018

@author: nabil
"""

from selenium import webdriver
import time


"""
Ladepeche
"""
def connect_ldpch(email, passwrd):
    url = "https://www.ladepeche.fr/"
    driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    driver.get(url)
    driver.set_window_size(1120, 550)
    email = "watchnewsapp@gmail.com"
    passwrd = "projetsid2018"
    # Cliquer sur connexion
    driver.find_element_by_xpath(('//a[contains(@onclick,"login")]')).click()
    time.sleep(3)
    # Locliser et remplir les champs
    driver.find_element_by_id("user_login").send_keys(email)
    driver.find_element_by_id("user_pass").send_keys(passwrd)
    time.sleep(3)
    # Click sur connexion
    driver.find_element_by_id('submit-login').click()
    time.sleep(10)
    # Saves the screenshot
    driver.save_screenshot("/Users/nabil/Desktop/Projet/testLogin/ladepecheee.png")
    driver.quit()


"""
Liberation
"""
def connect_lbrt(email, passwrd):
    url_log = "https://token.liberation.fr/accounts/login/"
    driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    # Donwlowad the website
    driver.get(url_log)
    driver.set_window_size(1120, 550)
    time.sleep(3)
    # Locliser et remplir les champs
    driver.find_element_by_id("id_email").send_keys(email)
    driver.find_element_by_id("id_password").send_keys(passwrd)
    # Click sur connexion
    driver.find_element_by_xpath('//input[@value="Me connecter"]').click()
    time.sleep(10)
    # Screen
    driver.save_screenshot("/Users/nabil/Desktop/Projet/testLogin/lib.png")
    driver.quit()


"""
Le nouvel obs
"""
def connect_obs(email, passwrd):
    url_obs = "https://www.nouvelobs.com"
    browser = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    browser.get(url_obs)
    time.sleep(3)
    # Cliquer sur connexion
    browser.find_element_by_xpath(('//label[contains(@for,"modal-one")]')).click()
    time.sleep(3)
    # Locliser les champs
    browser.find_element_by_id("name").send_keys(email)
    browser.find_element_by_id("passwd").send_keys(passwrd)
    time.sleep(3)
    # Click sur connexion
    browser.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(10)
    browser.save_screenshot("/Users/nabil/Desktop/Projet/testLogin/obs.png")
    browser.quit()


"""
l'equipe
"""
def connect_eqp(email, passwrd):
    url_eqp = "https://www.lequipe.fr"
    browser = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    browser.get(url_eqp)
    time.sleep(3)
    browser.find_element_by_xpath('//div/a[contains(@class,"icon--user")]').click()
    time.sleep(3)
    browser.find_element_by_name("username").send_keys(email)
    browser.find_element_by_name("password").send_keys(passwrd)
    browser.find_element_by_xpath('//a[contains(@class,"submit")]').click()
    time.sleep(10)
    browser.save_screenshot("/Users/nabil/Desktop/Projet/testLogin/eqp.png")
    browser.quit()


if __name__ == '__main__':
    email = "watchnewsapp@gmail.com"
    passwrd = "projetsid2018"
    connect_ldpch(email, passwrd)
    connect_eqp(email, passwrd)
    connect_obs(email, passwrd)
    connect_lbrt(email, passwrd)
