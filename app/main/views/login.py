from flask import current_app,render_template, session, redirect, flash, url_for
from app.main import main
from app.main.form import UserLogin
from app.main.models import AccountsData, UserPersonalData
from app import db
import requests
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import uniform
import os
from app.url_api import URL_API


@main.route("/login", methods=['GET', 'POST'])
def login(): 
    form = UserLogin()
    if form.validate_on_submit():
        password = form.password.data
        email = form.username.data + '@' + form.email.data
        _token =requests.post(URL_API+'tokens/', auth=(email,password))
        if _token.status_code==200:
            
            session['token'] = _token.json()['token']
            email = session['token']
            password = ''
            _tags =requests.get(URL_API+'tags/', auth=(email,password))
            if _tags.status_code==200:
                session['tags'] = _tags.json()
                session['not_follow_back']=None
                browser = current_app.browser
                browser.get('https://www.instagram.com/')
                sleep(uniform(2,3))
                
                #click en 'ahora no' par ventanas emergentes
                from app import bot_config_api as config
                try :
                    not_now = browser.find_element_by_xpath(config.login["NOT_NOW"])
                    not_now.click()
                except NoSuchElementException:
                    next
                sleep(uniform(1,2))
                
                try :
                    not_now = browser.find_element_by_xpath(config.login["NOT_NOW"])
                    not_now.click()
                except NoSuchElementException:
                    next
                
                
                try:
                    browser.find_element_by_css_selector(config.login["USERNAME_INPUT"])
                    flash('Al parecer no hay ninguna sesión de Instagram iniciada en tu navegador, por favor inicia sesión en Instagram con el siguiente formulario.','primary')
                    return redirect(url_for('.login_ig'))
                except NoSuchElementException:
                    try:
                        change_account = browser.find_element_by_xpath(config.login["CHANGE_ACCOUNT"])
                        sleep(uniform(1,2))
                        change_account.click()
                        flash('Al parecer no hay ninguna sesión de Instagram iniciada en tu navegador, por favor inicia sesión en Instagram con el siguiente formulario.','primary')
                        return redirect(url_for('.login_ig'))
                    except NoSuchElementException:
                        try:
                            browser.find_element_by_css_selector(config.input_search["HASHTAG_INPUT"])
                            username = browser.find_element_by_css_selector(config.login["USERNAME"])
                            session['username'] = username.text
                            data_query = UserPersonalData.query.filter_by(ig_username=username.text).first()
                            if data_query is None: 
                                personal_data = UserPersonalData(ig_username=username.text)
                                db.session.add(personal_data)
                                db.session.commit()
                            return redirect(url_for('.seguir'))
                        except NoSuchElementException:
                            try:
                                browser.find_element_by_css_selector(config.input_search["HASHTAG_INPUT_B"])
                                username = browser.find_element_by_css_selector(config.login["USERNAME"])
                                data_query = UserPersonalData.query.filter_by(ig_username=username.text).first()
                                if data_query is None: 
                                    personal_data = UserPersonalData(ig_username=username.text)
                                    db.session.add(personal_data)
                                    db.session.commit()
                                session['username'] = username.text
                                
                                try:
                                    profile_img = browser.find_element_by_xpath(f"//img[contains(@alt,'{username.text}')]")
                                except NoSuchElementException:
                                    email = session['token']
                                    password=''
                                    requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.login["IMG_PROFILE"], 'tag_id':(config.tags['IMG_PROFILE'])['id']}]})
                                    flash('En estos momentos nos encontramos en mantenimiento, gracias.','danger')
                                    return redirect(url_for('.login'))

                                session['img_profile'] = profile_img.get_attribute('src')
                                return redirect(url_for('.seguir'))
                            except NoSuchElementException:
                                email = session['token']
                                password=''
                                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.input_search["HASHTAG_INPUT_B"], 'tag_id':(config.tags['HASHTAG_INPUT_B'])['id']}]})
                                flash('En estos momentos nos encontramos en mantenimiento, gracias.','danger')
                                return redirect(url_for('.login'))
            else:
                flash('Tu nombre de usuario o contraseña son incorrectos.','danger')
                return redirect(url_for('.login'))
        else:
            flash('Tu nombre de usuario o contraseña son incorrectos.','danger')
            return redirect(url_for('.login'))

    return render_template("login.html", form = form)

