from flask import render_template, session, flash, current_app, redirect, url_for, g
from app.main import main
from app.main.form import NotFollowBack
from app.exceptions import NormalError, NoAllFollowers
from app.main.models import FollowsData, BotCampaing
from datetime import datetime
from app import db

@main.route("/not-follow-back",methods=['GET', 'POST'])
def not_follow_back():
    form = NotFollowBack()
    try:
        n_following = session['following']
        n_followers = session['followers']
    except KeyError:
        n_following = 0 
        n_followers = 0

    try:
        not_follow_back = current_app.not_follow_back
    except AttributeError:
        not_follow_back = None

    if form.validate_on_submit():
        from app.Bot_ig import autoig
        username = session['username']
        browser = current_app.browser
        ig = autoig(browser, username)
        
        not_follow_back = ig.get_unfollowers(username)
        followers = ig.followers
        following = ig.following
        n_followers = int(ig.n_followers)
        n_following = int(ig.n_following)
        current_app.not_follow_back = not_follow_back

        if len(followers)<=n_followers+1:
            session['followers'] = len(followers)
        else:
            session['followers'] = n_followers
        if len(following)<=n_following+1:
            session['following'] = len(following)
        else:
            session['following'] = n_following

        if (len(followers) >= (n_followers - 5)) and (len(following) >= (n_following - 5)):
            ig.save_data(not_follow_back, 'not_follow_back.json')
            return redirect(url_for('main.not_follow_back'))
        else:
            ig.save_data(not_follow_back, 'not_follow_back.json')
            flash(f'No se ha completado la recolección de datos, el numero de seguidores obtenido fue {len(followers)} y de seguidos {len(following)}, vuelve a intentarlo más tarde.','primary')
            return redirect(url_for('.not_follow_back'))

    return render_template("not_follow_back.html", form=form, not_follow_back=not_follow_back, n_following=n_following, n_followers=n_followers)
