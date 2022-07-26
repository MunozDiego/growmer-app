
from flask import render_template, session, flash, current_app, redirect, url_for
from app.main import main
from app.main.form import UserFollowAdvanced
from app.exceptions import NormalError
from app.main.models import FollowsData, BotCampaing, UserPersonalData
from datetime import datetime
from time import time
from app import db
from random import uniform

@main.route("/seguir-advanced",methods=['GET', 'POST'])
def seguir_advanced():
    form = UserFollowAdvanced()
    if form.validate_on_submit():
        follows = FollowsData.query.all()
        follow_data = []
        seed = form.seed.data
        n_follows = form.n_follows.data
        n_min_followers = form.n_min_followers.data
        n_max_followers = form.n_max_followers.data
        post_min_requirement = form.post_min_requirement.data
        delta_down = form.delta_down.data
        if delta_down[-1] == '%':
            delta_down = float(delta_down.strip('%'))/100
        else:
            delta_down = float(delta_down)/100
        delta_up = form.delta_up.data
        n_max_following = form.n_max_following.data
        time_lag_up = form.time_lag_up.data
        time_lag_down = form.time_lag_down.data

        today = datetime.utcnow().strftime('%d-%m-%Y')
        today_follow = 0
        for campaing in BotCampaing.query.filter_by(str_date=today):
            today_follow += campaing.n_follows 

        if today_follow >=200:
            flash('Has excedido él limite de 200 follows por día.', 'warning')
            return redirect(url_for('main.seguir_advanced'))
            
        from app.Bot_ig import autoig
        username = session['username']
        browser = current_app.browser
        ig = autoig(browser, username)


        star_t = time()
        try:
            ig.follow_strategy(seed, n_follows, n_min_followers = n_min_followers, n_max_followers = n_max_followers, post_min_requirement = post_min_requirement,\
                        delta_down = delta_down, delta_up = delta_up, n_max_following = n_max_following, follow_data = follow_data, \
                            users_viwed = follows, new_user_requirement = True, time_lag = uniform(time_lag_down,time_lag_up))
        except NormalError:
            n_follows = len(follow_data)
            flash(f'Ha ocurrido un error inesperado, seguiste {n_follows} perfiles en la sesión, si no es el numero que esperabas por favor vuelve a intentarlo. Puedes comunicar este error a support@growmer.com','danger')
            return redirect(url_for('.seguir_advanced'))
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
        return redirect(url_for('.seguir_advanced'))

    return render_template("seguir-advanced.html", form=form)
