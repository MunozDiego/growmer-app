# -*- coding: utf-8 -*-
"""
Bot build upon Selenium to Growmer App Free
"""

import os
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time
from random import randint, uniform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from datetime import datetime    
from . import bot_config_api  as config
from app.url_api import URL_API
import requests
from flask import session
from .exceptions import NoPostAvailable,NoFollowersAvailable,NormalError,NoAllFollowers,TimeOut
from itertools import count

#%%
class autoig:
    def __init__(self, browser, username):
        self.browser = browser
        self.username = username

    #function to send a warning to growmer api, add a body tag filter and a time limit to render the DOM
    #try to evit all falase positive warnings
    def find_element_with_warning_post(self, tag):
        body = None
        selector=(config.tags[tag])['selector']
        star_time = time()
        while body == None:
            try:
                body = self.browser.find_element_by_css_selector('body')
            except NoSuchElementException:
                body = None
                current_time = time()
                if current_time - star_time > 30:
                    break

        if body != None:
            try:
                if selector == 'css':
                    element = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, (config.tags[tag])['tag']))
                    )
                else:
                    element = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, (config.tags[tag])['tag']))
                    )
                return element
            except TimeoutException:
                email = session['token']
                password=''
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': (config.tags[tag])['tag'], 'tag_id':(config.tags[tag])['id']}]})
                raise NormalError
        else:
            raise TimeOut

    #login instagram
    #click in 'not now' button twoice, this could be a choice with remember me button
    def login(self, password):
        
        username_input = self.find_element_with_warning_post(tag = "USERNAME_INPUT")

        password_input = self.find_element_with_warning_post(tag = "PASSWORD_INPUT")

        username_input.send_keys(self.username)
        password_input.send_keys(password)

        login_button = self.find_element_with_warning_post(tag = "LOGIN_BUTTON")

        login_button.click()
        
        sleep(uniform(2,3))
        
        #click en 'ahora no' par ventanas emergentes
        try :
            not_now = self.browser.find_element_by_xpath(config.login["NOT_NOW"])
            not_now.click()
        except NoSuchElementException:
            next
        sleep(uniform(1,2))
        
        try :
            not_now = self.browser.find_element_by_xpath(config.login["NOT_NOW"])
            not_now.click()
        except NoSuchElementException:
            next
            
        sleep(uniform(2,3))      
        
    #Get not follow back users
    def get_unfollowers(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        sleep(uniform(3,5))

        following_button = self.find_element_with_warning_post(tag = "FOLLOWING_BUTTON")
        following_button.click()

        #store data 
        self.n_following = self.find_element_with_warning_post(tag = "N_FOLLOWING").text
        sleep(uniform(3,5)) 

        self.following = self._get_names()

        followers_button = self.find_element_with_warning_post(tag = "FOLLOWERS_BUTTON")
        followers_button.click()
        
        self.n_followers = self.find_element_with_warning_post(tag = "N_FOLLOWERS").text

        self.followers = self._get_names()
        
        not_following_back = [user for user in self.following if user not in self.followers]
        return not_following_back
    
    #Aply a loop to be sure of a complete list, currently growmer dont use it
    def get_not_follow_back(self,username):
        star_t=time()
        success = False
        while success == False:
            not_following_back = self.get_unfollowers(username = username)
            followers = self.followers
            following = self.following
            n_followers = int(self.n_followers)
            n_following = int(self.n_following)
            if (len(followers) >= (n_followers - 5)) and (len(following) >= (n_following - 5)):
                success = True
                self.not_following_back = not_following_back
                return not_following_back
            else:
                success = True
                self.not_following_back = not_following_back
                end_t=time()
                raise NoAllFollowers

    #Get the usernames from the box with the list of users
    def _get_names(self):
        sleep(uniform(1,2))

        scroll_box = self.find_element_with_warning_post(tag = "SCROLL_BOX")

        start_t=time()
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.browser.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
            current_time=time()
            if current_time-start_t>1200:
                last_ht=ht
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        # close button
        close_button = self.find_element_with_warning_post(tag = "CLOSE_BUTTON")
        close_button.click()
        return names
    
    #unfollow with a list of usernames
    def unfollowWithUsername(self, names, time_slap=uniform(15,20)):
        for name in names:
            self.browser.get('https://www.instagram.com/' + name + '/')
            sleep(time_slap)
            
            followButton = self.find_element_with_warning_post(tag = "UNFOLLOW_BUTTON")
            sleep(uniform(2,3))  
            followButton.click()

            confirmButton = self.find_element_with_warning_post(tag = "CONFIRMBUTTON")
            confirmButton.click()
            sleep(uniform(3,5)) 
        
    #Follow requirement to use in follow strategy
    #fix a 1k issue in te instagram format, the limit is 9999 wich correspond to 9k
    def _requirement_profile(self,n_post, n_followers, n_following, n_min_followers, n_max_followers,\
                                    post_min_requirement, delta_down, delta_up, n_max_following, \
                                        users_viwed, user_name, new_user_requirement) :
        try:
            n_post=int(n_post)
        except ValueError:
            n_post=int(n_post[0]+n_post[-3:])
            
            
        try:
            n_followers=int(n_followers)
        except ValueError:
            try:
                n_followers=int(n_followers[0]+n_followers[-3:])
            except ValueError:
                try:
                    n_followers=int(n_followers[0:2]+n_followers[-2:-1])*100
                except ValueError:
                    n_followers=int(n_followers[0:3]+n_followers[-2:-1])*100    
            
        try:
            n_following=int(n_following)
        except ValueError:
            try:
                n_following=int(n_following[0]+n_following[-3:])
            except ValueError:
                try:
                    n_following=int(n_following[0:2]+n_following[-2:-1])*100
                except ValueError:
                    n_following=int(n_following[0:3]+n_following[-2:-1])*100 
    
        if new_user_requirement:
            if n_post > post_min_requirement and \
                n_min_followers < n_followers < n_max_followers and \
                (n_followers*delta_down) < n_following < (n_followers+delta_up) and \
                n_following < n_max_following and \
                    user_name not in users_viwed :
                return True
            else:
                return False
        else:
            if n_post > post_min_requirement and \
                n_min_followers < n_followers < n_max_followers and \
                (n_followers*delta_down) < n_following < (n_followers+delta_up) and \
                n_following < n_max_following:
                return True
            else:
                return False
        
    #determine if an account is public or private
    def _public_account(self):
        try:
            self.browser.find_element_by_xpath(config.public_account["PUBLIC_ACCOUNT"])
            return False
        except NoSuchElementException:
            return True
    
    #Make a search in the search bar, sometimes fail 
    def _input_search(self, _seed):
    
        try:
            hashtag_input = self.browser.find_element_by_css_selector(config.input_search["HASHTAG_INPUT"])
        except NoSuchElementException:
            hashtag_input = self.find_element_with_warning_post(tag = "HASHTAG_INPUT_B")

        hashtag_input.send_keys(_seed)
        sleep(uniform(1,1.5))
        hashtag_input.send_keys(Keys.ENTER)
        sleep(uniform(2,3))
        try:
            hashtag_input.send_keys(Keys.ENTER)
        except StaleElementReferenceException:
            pass
        sleep(uniform(3,5))
    
    #A fix of follow strategy, some post dont have enough like when the requirements are hight, this scrap a second post
    #and raise an error if the like are not enough again.
    def follow_strategy(self, _seed, n_follows = 20, n_min_followers = 0, n_max_followers = 9999, post_min_requirement = 0,\
                 delta_down = 0.6, delta_up = 9999, n_max_following = 9999, follow_data = [], \
                      users_viwed = [], new_user_requirement = True, time_lag = uniform(30,60)):

        #ir al perfil del usuario seed a traves del buscador
        #scrap a los likes de la primera publicacion
        #ir a los perfiles de dichos usuarios, si cumple requisito, seguir.
        self._input_search(_seed)
        
        #se hace un test porque se necesita la lista de posts, pero el comand que retorna la lista, si no encuentra nada,
        #retorna una lista vacia, por lo que no arroja ninguna exception
        post_to_scrape_test = self.find_element_with_warning_post(tag = "POST_TO_SCRAPE")
        
        random_post = randint(0,8)
        self.actual_follows = 0
        print(f'actual_follows: {self.actual_follows}')

        try:
            self._follow_strategy(random_post=random_post, n_follows = n_follows, n_min_followers = n_min_followers, n_max_followers = n_max_followers, post_min_requirement = post_min_requirement,\
                delta_down = delta_down, delta_up = delta_up, n_max_following = n_max_following, follow_data = follow_data, \
                    users_viwed = users_viwed, new_user_requirement = new_user_requirement, time_lag = time_lag)
            print(f'actual_follows after: {self.actual_follows}')
        except IndexError:
            close_list_button = self.browser.find_elements_by_css_selector(config.get_names["CLOSE_BUTTON"])[1]#se selecciona el segundo elemento porque esta el pop up de la publicacion y el de likes
            close_list_button.click()
            sleep(uniform(2,3))
            
            close_post_button = self.find_element_with_warning_post(tag = "CLOSE_BUTTON")
            close_post_button.click()
            sleep(uniform(2,3))
            if random_post != 0:
                random_post = 0
            else:
                random_post = randint(1,8)
            try:
                self._follow_strategy(random_post=random_post, n_follows = n_follows, n_min_followers = n_min_followers, n_max_followers = n_max_followers, post_min_requirement = post_min_requirement,\
                    delta_down = delta_down, delta_up = delta_up, n_max_following = n_max_following, follow_data = follow_data, \
                        users_viwed = users_viwed, new_user_requirement = new_user_requirement, time_lag = time_lag)
            except IndexError:
                raise NormalError

    #search the seed, get usernames from like list of a popular post, evaluate follow or not         
    def _follow_strategy(self, random_post, n_follows, n_min_followers, n_max_followers, post_min_requirement,\
                 delta_down, delta_up, n_max_following, follow_data, \
                      users_viwed, new_user_requirement, time_lag):

        post_to_scrape = self.browser.find_elements_by_css_selector(config.follow_strategy["POST_TO_SCRAPE"])[random_post]
        post_to_scrape.click()
        sleep_time_1 = uniform(5, 10)
        sleep(sleep_time_1)
        
        like_list = self.find_element_with_warning_post(tag = "LIKE_LIST")
        like_list.click()
        sleep(uniform(3,5))
        
        #tambien es un test de un elemento del cual se necesita una lista
        profile_list = self.find_element_with_warning_post(tag = "PROFILE_LIST")

        users_viwed_now = []
        exceptions_n_post = []
        exceptions_n_followers = []
        exceptions_n_following = []

        for n in count(1):
                
            profile_list = self.browser.find_elements_by_css_selector(config.follow_strategy["PROFILE_LIST"])
            if n < 12:
                profile = profile_list[n].find_element_by_css_selector("a") 
                print('       ' + str(profile_list[n].find_element_by_css_selector("a").text))    
                    
            else:
                profile = profile_list[12].find_element_by_css_selector("a")
                print('       ' + str(profile_list[12].find_element_by_css_selector("a").text))
            sleep(uniform(3,5))
            print(n)
            
            if profile.text in users_viwed_now:
                next                
            else:
                users_viwed_now.append(profile.text)
                profile.send_keys(Keys.CONTROL + Keys.RETURN)
                sleep(uniform(2,2.5))
                self.browser.switch_to.window(self.browser.window_handles[1])
                sleep(uniform(8,12))

                if self._public_account():
                    try:
                        user_name = self.browser.find_element_by_css_selector('h2').text
                    except NoSuchElementException:
                        user_name = self.browser.find_element_by_css_selector('h1').text

                    try:
                        n_post =self.browser.find_element_by_xpath(config.follow_strategy['N_POST']).text       
                    except NoSuchElementException:
                        #si da 3 errores seguidos, envia el error a la api
                        exceptions_n_post.append(n)
                        n_post = 0
                        if len(exceptions_n_post)>=3:
                            if (exceptions_n_post[1]==(exceptions_n_post[0]+1)) and (exceptions_n_post[2]==(exceptions_n_post[0]+2)):
                                email = session['token']
                                password=''
                                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.follow_strategy['N_POST'], 'tag_id':(config.tags['N_POST'])['id']}]})
                                raise NormalError

                    try:
                        n_followers =self.browser.find_element_by_xpath(config.follow_strategy["N_FOLLOWERS"]).text
                    except NoSuchElementException:
                        #si da 3 errores seguidos, envia el error a la api
                        exceptions_n_followers.append(n)
                        n_followers = 0
                        if len(exceptions_n_followers)>=3:
                            if (exceptions_n_followers[1]==(exceptions_n_followers[0]+1)) and (exceptions_n_followers[2]==(exceptions_n_followers[0]+2)):
                                email = session['token']
                                password=''
                                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.follow_strategy["N_FOLLOWERS"], 'tag_id':(config.tags['N_FOLLOWERS'])['id']}]})
                                raise NormalError

                    try:
                        n_following = self.browser.find_element_by_xpath(config.follow_strategy["N_FOLLOWING"]).text
                    except NoSuchElementException:
                        #si da 3 errores seguidos, envia el error a la api
                        exceptions_n_following.append(n)
                        n_following = 0
                        if len(exceptions_n_following)>=3:
                            if (exceptions_n_following[1]==(exceptions_n_following[0]+1)) and (exceptions_n_following[2]==(exceptions_n_following[0]+2)):
                                email = session['token']
                                password=''
                                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.follow_strategy["N_FOLLOWING"], 'tag_id':(config.tags['N_FOLLOWING'])['id']}]})
                                raise NormalError

                    date = datetime.utcnow()
                    scrape_data = [date, user_name]
                    
                    if self._requirement_profile(n_post, n_followers, n_following, n_min_followers, n_max_followers,\
                                                post_min_requirement, delta_down, delta_up, n_max_following, \
                                                    users_viwed, user_name, new_user_requirement):
                        try:
                            follow_button = self.find_element_with_warning_post(tag = "FOLLOW_BUTTON")
                            follow_button.click()
                            sleep_time_2 = time_lag
                            sleep(sleep_time_2)
                            self.actual_follows +=1
                            follow_data.append(scrape_data)
                            if n_follows == self.actual_follows:
                                self.browser.close()
                                self.browser.switch_to.window(self.browser.window_handles[0])
                                break
                        except NoSuchElementException:
                            print('you already follow this account')
                else:
                    next                
                    
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])

        close_list_button = self.browser.find_elements_by_css_selector(config.get_names["CLOSE_BUTTON"])[1]#se selecciona el segundo elemento porque esta el pop up de la publicacion y el de likes
        close_list_button.click()
        sleep(uniform(2,3))
        
        close_post_button = self.find_element_with_warning_post(tag = "CLOSE_BUTTON")
        close_post_button.click()
        sleep(uniform(2,3))
        
        home_ig = self.find_element_with_warning_post(tag = "HOME_IG")
        home_ig.click()
        sleep(uniform(2,3))
    
    #self explanatory
    def get_info_profile(self,n_photos_to_scrap, self_data = []):
        
        self.browser.get('https://www.instagram.com/' + self.username + '/')
        
        sleep(uniform(3,5))
        #Datos a almacenar
        
        n_post = self.find_element_with_warning_post(tag = "N_POST")

        n_followers = self.find_element_with_warning_post(tag = "N_FOLLOWERS")

        n_following = self.find_element_with_warning_post(tag = "N_FOLLOWING")

        date = datetime.now()

        if int(n_post)>=10:
            new_post = self.find_element_with_warning_post(tag = "POST_TO_SCRAPE")
            new_post.click()
            sleep_time_3 = uniform(5, 10)
            sleep(sleep_time_3)

            n_photos = 0
            scrape_data_photos = []
            exceptions_like= []
            exceptions_comment= []
            while n_photos < n_photos_to_scrap:
                try:
                    #fecha
                    time_from_publish = self.find_element_with_warning_post(tag = "TIME_FROM_PUBLISH")
                        
                    #n_likes
                    try:
                        likes = self.browser.find_element_by_xpath(config.get_info_profile["LIKES"]).text
                    except NoSuchElementException:
                        exceptions_like.append(n_photos)
                        like = 0
                        if len(exceptions_like)>=3:
                            if (exceptions_like[1]==(exceptions_like[0]+1)) and (exceptions_like[2]==(exceptions_like[0]+2)):
                                email = session['token']
                                password=''
                                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.get_info_profile["LIKES"], 'tag_id':(config.tags['LIKES'])['id']}]})
                                raise NormalError

                    #n_comment  TESTEAR DE FORMA MANUAL
                    for n in range(1,9):
                        try:
                            more_comments = self.browser.find_element_by_css_selector(config.get_info_profile["MORE_COMMENTS"])
                            more_comments.click()
                            
                            sleep_time = uniform(2,2.5)
                            sleep(sleep_time)
                        except NoSuchElementException:
                            break

                    try:
                        ul_comment_test = self.browser.find_element_by_css_selector(config.get_info_profile["UL_COMMENT"])
                    except NoSuchElementException:
                        exceptions_comment.append(n_photos)
                        ul_comment = []
                        if len(exceptions_comment)>=5:
                            if (exceptions_comment[1]==(exceptions_comment[0]+1)) and (exceptions_comment[4]==(exceptions_comment[0]+4)):
                                email = session['token']
                                password=''
                                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.get_info_profile["UL_COMMENT"], 'tag_id':(config.tags['UL_COMMENT'])['id']}]})
                                raise NormalError
                    
                    ul_comment = self.browser.find_elements_by_css_selector(config.get_info_profile["UL_COMMENT"])

                    #n_comment
                    n_comments = len(ul_comment)
                    
                    scrape_data_photo = [n_photos,time_from_publish, likes, n_comments]
                    scrape_data_photos.append(scrape_data_photo)

                    next_post_user = self.find_element_with_warning_post(tag = "NEXT_POST_USER")
                    next_post_user.click() 
                
                    sleep_time_4 = uniform(10, 15)
                    sleep(sleep_time_4)
                    
                    n_photos += 1
                    
                except NoSuchElementException:
                    break

        else:
            scrape_data_photos = []
            n_photos = 0
            time_from_publish = [0]
            n_likes = [0]
            n_comments = [0]
            scrape_data_photo = [n_photos,time_from_publish, n_likes, n_comments]
            scrape_data_photos.append(scrape_data_photo)

        
        #Se guarda todo en una lista de listas
        scrape_data = [date, n_post, n_followers, n_following, scrape_data_photos]
        self_data.append(scrape_data)   
        
    #get only followers from followers list, get names function used
    def GetFollowers(self):
        
        star_t = time()
        success = False
        while success == False:
            self.browser.get('https://www.instagram.com/' + self.username + '/')
            sleep(uniform(2,3))
     
            try:
                n_followers =self.browser.find_element_by_xpath(config.get_followers['N_FOLLOWERS']).text
            except NoSuchElementException:
                email = session['token']
                password=''
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.get_followers['N_FOLLOWERS'], 'tag_id':(config.tags['N_FOLLOWERS'])['id'], 'status': 'warning'}]})
                raise NoFollowersAvailable

            try:
                followers_button = self.browser.find_element_by_xpath(config.get_followers['FOLLOWERS_BUTTON'])
            except NoSuchElementException:
                email = session['token']
                password=''
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.get_followers['FOLLOWERS_BUTTON'], 'tag_id':(config.tags['FOLLOWERS_BUTTON'])['id']}]})
                raise NormalError

            followers_button.click()

            followers = self._get_names()

            try:
                n_followers=int(n_followers)
            except ValueError:
                try:
                    n_followers=int(n_followers[0]+n_followers[-3:])
                except ValueError:
                    try:
                        n_followers=int(n_followers[0:2]+n_followers[-2:-1])*100
                    except ValueError:
                        try:
                            n_followers=int(n_followers[0:3]+n_followers[-2:-1])*100
                        except ValueError:
                            raise TimeOut
                        
            if len(followers) >= (int(n_followers)-5):
                success = True
                return followers
            else:
                success = False
                self.restart_session()
                end_t=time()
                if (end_t-star_t)>=300:
                    raise NoAllFollowers
                else:
                    sleep(uniform(20,30))

    #change instagram accounts, somtimes the word is 'cerrar sesión' and other is 'salir', dontknow exactly why
    #could change by language or randomly
    def change_account(self):

        drop = self.find_element_with_warning_post(tag = 'IMG_DROP')
        drop.click()
        sleep(uniform(2,2.5))

        #aveces renderizan salir, otras veces cerrar sasion ¿podrian ser mas?
        try:
            _exit = self.browser.find_element_by_xpath(config.change_account['EXIT'])
            _exit.click()
        except NoSuchElementException:
            try:
                _logout = self.browser.find_element_by_xpath(config.change_account['LOGOUT'])
                _logout.click()
            except NoSuchElementException:
                email = session['token']
                password=''
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.change_account['EXIT'], 'tag_id':(config.tags['EXIT'])['id']}]})
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.change_account['LOGOUT'], 'tag_id':(config.tags['LOGOUT'])['id']}]})
                raise NormalError
        sleep(uniform(4,5))

        change_account = self.find_element_with_warning_post(tag = "CHANGE_ACCOUNT")

        try:
            change_account = self.browser.find_element_by_xpath(config.login['CHANGE_ACCOUNT'])
            change_account.click()
        except NoSuchElementException:
            try:
                username_test = self.browser.find_element_by_css_selector(config.login['USERNAME_INPUT'])
            except NoSuchElementException:
                email = session['token']
                password=''
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.login['CHANGE_ACCOUNT'], 'tag_id':(config.tags['CHANGE_ACCOUNT'])['id']}]})
                raise NormalError

        sleep(uniform(1,2))


    #carga archivo de datos de tipo json    
    def load_data(self, data):
        with open(str(data), "r") as f:
            likes_data = json.load(f)
            return likes_data
    #guarda archivo de datos de tipo json, pasando tipo date a str  
    def save_data(self, data, _as):
        with open(str(_as), "w") as f:
            json.dump(data, f, indent=4, sort_keys=True, default=str)
    
    #cambia el foco del webdriver a la pestaña 0 y va al inicio de ig
    def restart_session(self):
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.get('https://www.instagram.com/')

    def login_success(self):
        try:
            self.browser.find_element_by_css_selector("p[role='alert']")#cuidado con esta
            login = False
        except NoSuchElementException:
            login = True
        return login
            
    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()
            



