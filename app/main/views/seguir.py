
from flask import render_template, session, flash, current_app, redirect, url_for
from app.main import main
from app.main.form import UserFollow
from app.exceptions import NormalError
from app.main.models import FollowsData, BotCampaing, UserPersonalData
from datetime import datetime
from time import time
from app import db
from random import uniform


@main.route("/seguir", methods=['GET', 'POST'])
def seguir():
    form = UserFollow()
    if form.validate_on_submit():
        follows = FollowsData.query.all()
        follow_data = []
        seed = form.seed.data
        n_follows = form.n_follows.data

        today = datetime.utcnow().strftime('%d-%m-%Y')
        today_follow = 0
        for campaing in BotCampaing.query.filter_by(str_date=today):
            today_follow += campaing.n_follows 

        if today_follow >=200:
            flash('Has excedido él limite de 200 follows por día.', 'warning')
            return redirect(url_for('.seguir'))

        from app.Bot_ig import autoig
        username = session['username']
        browser = current_app.browser
        ig = autoig(browser, username)

        star_t = time()
        try:
            ig.follow_strategy(seed, n_follows, n_min_followers = 30, n_max_followers = 1500, post_min_requirement = 3,\
                    delta_down = 0.6, delta_up = 800, n_max_following = 2000, follow_data = follow_data, \
                        users_viwed = follows, new_user_requirement = True, time_lag = uniform(60,120))
        except NormalError:
            n_follows = len(follow_data)
            flash(f'Ha ocurrido un error inesperado, seguiste {n_follows} perfiles en la sesión, si no es el numero que esperabas por favor vuelve a intentarlo. Puedes comunicar este error a support@growmer.com','danger')
            return redirect(url_for('.seguir'))
        end_t = time()

        
        #add campaing data 
        n_follows = len(follow_data)
        total_time= end_t - star_t
        date = datetime.utcnow()
        user = UserPersonalData.query.filter_by(ig_username=username).first()
        campaing = BotCampaing(date=date, str_date=date.strftime('%d-%m-%Y'),n_follows=n_follows,duration = total_time, user_id=user.id)
        db.session.add(campaing)
        db.session.commit()

        bot_session = BotCampaing.query.order_by(BotCampaing.id.desc()).first()
        

        #add user names to followsdata
        for user in follow_data:
            to_commit = FollowsData(ig_username = user[1], campaing = bot_session.id)
            db.session.add(to_commit)
        db.session.commit()

        flash(f'Seguiste a {n_follows} perfiles en la sesión, si no es el número que esperabas por favor vuelve a intentarlo. Puedes comunicar este error a support@growmer.com','primary')
        return redirect(url_for('.seguir'))

    return render_template("seguir-usuarios.html", form=form)
