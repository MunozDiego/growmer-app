from flask import render_template, session, flash, current_app, redirect, url_for
from app.main import main
from app.main.form import UserUnfollowAuto
from app.exceptions import NormalError, NoAllFollowers, TimeOut
from app.main.models import FollowsData, BotCampaing, UserPersonalData
from datetime import datetime
from app import db
from random import uniform


@main.route("/unfollow",methods=['GET', 'POST'])
def unfollow():
    form = UserUnfollowAuto()
    user = UserPersonalData.query.filter_by(ig_username=session['username']).first()
    form.date.choices = [(campaing.id,f"{campaing.str_date}({campaing.n_follows})") for campaing in BotCampaing.query.filter_by(unfollow=False).filter_by(user_id=user.id)]
    if form.date.choices==[]:
        use_follow_tool= "False"
    else:
        use_follow_tool="True"
    if form.validate_on_submit():
        campaign_id = form.date.data
        _campaign = BotCampaing.query.filter_by(id=campaign_id).first()
        campaign_in_date = FollowsData.query.filter_by(campaing=campaign_id)

        if _campaign.n_follows<50:
            time_slap = uniform(25,40)
        elif _campaign.n_follows<100:
            time_slap = uniform(40,60)
        elif _campaign.n_follows>100:
            time_slap = uniform(50,70)

        from app.Bot_ig import autoig
        username = session['username']
        browser = current_app.browser
        ig = autoig(browser, username)

        n_unfollows = 0
        name_unfollows = []
        if form.unfollow_all.data == True:
            try:
                followers = ig.GetFollowers()
            except NoAllFollowers:
                flash('Se ha superado el tiempo máximo de proceso, por lo que se ha detenido el bot, vuelve a intentarlo más tarde.','danger')
                return redirect(url_for('.unfollow'))
            except TimeOut:
                flash('Se ha superado el n° máximo de seguidores, por lo que se ha detenido el bot, vuelve a intentarlo más tarde.','danger')
                return redirect(url_for('.unfollow'))
            for user in campaign_in_date:
                username = user.ig_username
                if username not in followers:
                    try:
                        ig.unfollowWithUsername([username], time_slap=time_slap)
                        n_unfollows += 1
                        name_unfollows.append(username)
                    except NormalError:
                        flash(f'Ha ocurrido un error al intentar dejar de seguir a: {username}, puede ser que el usuario ya no este disponible. Vuelve a intentarlo más tarde.', 'warning')
                        return redirect(url_for('.unfollow'))
                else:
                    pass
        else:
            for user in campaign_in_date:
                username = user.ig_username
                try:
                    ig.unfollowWithUsername([username],time_slap=time_slap)
                    n_unfollows += 1
                    name_unfollows.append(username)
                except NormalError:
                        flash(f'Ha ocurrido un error al intentar dejar de seguir a: {username}, puede ser que el usuario ya no este disponible. Vuelve a intentarlo más tarde.', 'warning')
                        return redirect(url_for('.unfollow'))
        _campaign.auto_unfollow = n_unfollows
        _campaign.unfollow = True
        db.session.commit()
        #agregar commit para saber a quien ya dejaste de seguir
        flash(f'Has dejado de seguir a {n_unfollows} usuarios.', 'success')
        return redirect(url_for('.unfollow'))
    return render_template("dejar-seguir.html", form=form,use_follow_tool=use_follow_tool)

#lo mismo pero con query de todas las campañas, hay que cambiar esto para la siguiente version
@main.route("/unfollow_all",methods=['GET', 'POST'])
def unfollow_all():
    form = UserUnfollowAuto()
    user = UserPersonalData.query.filter_by(ig_username=session['username']).first()
    form.date.choices = [(campaing.id,f"{campaing.str_date}({campaing.n_follows})") for campaing in BotCampaing.query.filter_by(user_id=user.id).all()]
    if form.date.choices==[]:
        use_follow_tool= "False"
    else:
        use_follow_tool="True"
    if form.validate_on_submit():
        campaign_id = form.date.data
        _campaign = BotCampaing.query.filter_by(id=campaign_id)
        campaign_in_date = FollowsData.query.filter_by(campaing=campaign_id)

        if _campaign.n_follows<50:
            time_slap = uniform(25,40)
        elif _campaign.n_follows<100:
            time_slap = uniform(40,60)
        elif _campaign.n_follows>100:
            time_slap = uniform(50,70)

        from app.Bot_ig import autoig
        username = session['username']
        browser = current_app.browser
        ig = autoig(browser, username)

        n_unfollows = 0
        name_unfollows = []
        if form.unfollow_all.data == True:
            try:
                followers = ig.GetFollowers()
            except NoAllFollowers:
                flash('Se ha superado el tiempo máximo de proceso, por lo que se ha detenido el bot, vuelve a intentarlo más tarde.','danger')
                return redirect(url_for('.unfollow'))
            for user in campaign_in_date:
                username = user.ig_username
                if username not in followers:
                    try:
                        ig.unfollowWithUsername([username], time_slap=uniform(90,130))
                        n_unfollows += 1
                        name_unfollows.append(username)
                    except NormalError:
                        flash(f'Ha ocurrido un error al intentar dejar de seguir a: {username}, puede ser que el usuario ya no este disponible. Vuelve a intentarlo más tarde.', 'warning')
                        return redirect(url_for('.unfollow'))
                else:
                    pass
        else:
            for user in campaign_in_date:
                username = user.ig_username
                try:
                    ig.unfollowWithUsername([username],time_slap=uniform(90,130))
                    n_unfollows += 1
                    name_unfollows.append(username)
                except NormalError:
                        flash(f'Ha ocurrido un error al intentar dejar de seguir a: {username}, puede ser que el usuario ya no este disponible. Vuelve a intentarlo más tarde.', 'warning')
                        return redirect(url_for('.unfollow'))
        _campaign.auto_unfollow = n_unfollows
        _campaign.unfollow = True
        db.session.commit()
        #agregar commit para saber a quien ya dejaste de seguir
        flash(f'Has dejado de seguir a {n_unfollows} usuarios.', 'success')
        return redirect(url_for('.unfollow'))
    return render_template("dejar-seguir-query-all.html", form=form,use_follow_tool=use_follow_tool)
