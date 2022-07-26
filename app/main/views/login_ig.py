from flask import render_template, session, redirect, flash, url_for, current_app
from app.main import main
from app.main.form import UserLoginIg
from app.exceptions import NormalError
from app.main.models import AccountsData, UserPersonalData
from datetime import datetime
from app import db
from time import sleep
from random import uniform
from selenium.common.exceptions import NoSuchElementException
from app.url_api import URL_API


@main.route("/login_ig", methods=['GET', 'POST'])
def login_ig(): 
    form = UserLoginIg()
    if form.validate_on_submit():
        from app.Bot_ig import autoig
        password = form.password.data
        username = form.username.data
        session['current_account'] = form.username.data

        browser = current_app.browser
        try:
            ig = autoig(browser, username)
            ig.login(password)
        except NormalError:
            flash('El inicio de sesión no está disponible en estos momentos, por favor vuelve a intentarlo más tarde.', 'primary')
            return redirect(url_for('main.login_ig'))
        session['username'] = username        

        login_success = ig.login_success()
        
        if login_success:
            
            data_query = UserPersonalData.query.filter_by(ig_username=username).first()
            if data_query is not None: 
                account_id = data_query.id
            else:
                personal_data = UserPersonalData(ig_username=username)
                db.session.add(personal_data)
                db.session.commit()
                account_id = UserPersonalData.query.filter_by(ig_username=username).first()

            sleep(uniform(1.5,2))
            try:
                profile_img = browser.find_element_by_xpath(f"//img[contains(@alt,'{username}')]")
            except NoSuchElementException:
                email = session['token']
                password=''
                requests.post(URL_API+'warning_post/',auth=(email,password), json= {'warning': [{'tag_to_change': config.login["IMG_PROFILE"], 'tag_id':(config.tags['IMG_PROFILE'])['id']}]})
                flash('En estos momentos nos encontramos en mantenimiento, gracias.','danger')
                return redirect(url_for('.login'))

            session['img_profile'] = profile_img.get_attribute('src')

            return redirect(url_for('main.seguir'))
        else:
            flash('Tu nombre de usuario o contraseña son incorrectos.', 'danger')
            return redirect(url_for('main.login_ig'))
    return render_template("login_ig.html",  form = form)

@main.route('/new')
def change_account():
    browser = current_app.browser
    username = session['username']
    from app.Bot_ig import autoig
    ig = autoig(browser, username)
    try:
        ig.change_account()
        return redirect(url_for('main.login_ig'))
    except NormalError:
        flash('Ha ocurrido un error inesperado, vuelve a intentarlo más tarde. Te recomendamos que reinicies la aplicación.', 'danger')
        return redirect(url_for('main.login'))

