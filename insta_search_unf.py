from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import os

class InstaSearchUnf:
    driver = None
    def __init__(self, user_login, pw, user_searched, browser):
        if(user_login != "" and pw != ""):
            overwrite = self._verify_json(user_searched)
            if(overwrite):
                driver = self._get_browser(browser)
                driver.get('https://www.instagram.com')
                sleep(2)
                login_field = driver.find_element_by_xpath("//input[@name=\"username\"]")\
                    .send_keys(user_login)
                pw_field = driver.find_element_by_xpath("//input[@name=\"password\"]")\
                    .send_keys(pw)
                btn_login = driver.find_element_by_xpath('//button[@type="submit"]')\
                    .click()
                sleep(6)
                try:
                    driver.find_element_by_id('slfErrorAlert')
                    driver.quit()
                    messagebox.showwarning(title="Error", message="It seems your credentials are wrong! Try again")
                except:
                    driver.get('https://www.instagram.com/{}'.format(user_searched))
                    sleep(3.5)
                    btn_followers = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")\
                        .click()
                    self._get_actual_followers(driver)
            else:
                driver.quit()
        else:
            messagebox.showwarning(title="Error", message="All fields must be filled!")
        
    def _verify_json(self, user_searched):
        try:
            with open('user.json', 'r') as outfile:
                old_user = json.load(outfile)
                if(old_user != user_searched):
                    if messagebox.askyesno('Verify', 'This will overwrite the storaged data of {} and you will need to check this account again. Continue?'.format(old_user)):
                        with open('user.json', 'w') as outfile:
                            json.dump(user_searched, outfile)
                        with open('followers.json', 'w') as outfile:
                            json.dump('', outfile)
                        return True
                    else:
                        messagebox.showinfo('No', 'The script has been cancelled!')
                        return False
                else:  
                    return True
        except:
            with open('user.json', 'w') as outfile:
                json.dump(user_searched, outfile)
            return True
    
    def _get_actual_followers(self, driver):
       cont = 5
       running = True
       sleep(3)                                 
       initial = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[7]".format(cont))
       back = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[1]".format(cont))
       driver.execute_script('arguments[0].scrollIntoView(true);', initial)
       sleep(1)
       driver.execute_script('arguments[0].scrollIntoView(true);', back)
       sleep(1)
       
       target = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]".format(cont))
       while running:
            try:
                driver.execute_script('arguments[0].scrollIntoView(true);', target)
                cont += 5
                sleep(0.5)
                target = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]".format(cont))
            except:
                sleep(0.3)
                try:
                    driver.execute_script('arguments[0].scrollIntoView(true);', target)
                    cont += 5
                    sleep(0.5)
                    target = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]".format(cont))
                except:
                    running = False
       div_link = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div')
       links = div_link.find_elements_by_tag_name('a')
       names = [name.text for name in links if name.text != '']
       driver.quit()
       self._search_unf(names)

       with open('followers.json', 'w') as outfile:
            json.dump(names, outfile)

    def _search_unf(self, names):
        matches = False
        unfollowers = []
        try:    
            with open('followers.json', 'r') as outfile:
                json_followers = json.load(outfile)
        except:
            with open('followers.json', 'w') as outfile:
                json.dump(names, outfile)
            with open('followers.json', 'r') as outfile:
                json_followers = json.load(outfile)

        for old_followers in json_followers:
            for actual_followers in names:
                if(old_followers == actual_followers):
                    user_new = -1
                    matches = True
                elif(not matches):
                    user_new = old_followers
            if(user_new != -1):
                    unfollowers.append(user_new)
            matches = False
        if(unfollowers):
            messagebox.showwarning(title="Matches", message="Unfollowed by: {}".format(unfollowers))
        else:
            messagebox.showwarning(title="No matches", message="This account wasn't unfollowed by anyone!".format(unfollowers))
       
    def _get_browser(self, browser):
        cont = 0
        if(browser == 'Microsoft Edge'):
            for x in range(1, 4):
                try:
                    driver = webdriver.Edge('browser_drivers/msedgedriver_{}.exe'.format(x))
                except:
                    cont += 1
                    print("Wrong version")
        elif(browser == 'Opera'):
            for x in range(1, 4):
                try:
                    driver = webdriver.Opera('browser_drivers/operadriver_{}.exe'.format(x))
                except:
                    cont += 1
                    print("Wrong version")
        elif(browser == 'Google Chrome'):
            for x in range(1, 4):
                try:
                    driver = webdriver.Chrome('browser_drivers/chromedriver_{}.exe'.format(x))
                except:
                    cont += 1
                    print("Wrong version")
        elif(browser == 'Mozilla Firefox'):
            for x in range(1, 4):
                try:
                    driver = webdriver.Firefox('browser_drivers/geckodriver_{}.exe'.format(x))
                except:
                    cont += 1
                    print("Wrong version")
        else:
            messagebox.showwarning(title="Error", message="Select a browser!")
        
        if(cont == 3):
             messagebox.showwarning(title="Error", message="It seems you don't have this browser intalled! Please select another one")
        else:
            return driver 
