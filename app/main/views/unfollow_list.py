from flask import render_template, session, flash, current_app, redirect, url_for
from app.main import main
from app.main.form import UserUnfollowListText
from app.exceptions import NormalError
from datetime import datetime
from random import uniform


@main.route("/unfollow-list",methods=['GET', 'POST'])
def unfollow_list():
    form = UserUnfollowListText()
    if form.validate_on_submit():
        str_unfollow = form.user_list.data
        list_unfollow = str_unfollow.split(', ')

        from app.Bot_ig import autoig
        username = session['username']
        browser = current_app.browser
        ig = autoig(browser, username)
        if len(list_unfollow)<=50:
            time_slap=uniform(20,30)
        elif 50<len(list_unfollow)<=150:
            time_slap=uniform(60,90)
        elif 150<len(list_unfollow):
            time_slap=uniform(120,160)
        try:
            ig.unfollowWithUsername(list_unfollow, time_slap)
            flash('Has dejado de seguir a los usuarios de la lista exitosamente.', 'success')
            return redirect(url_for('.unfollow_list'))
        except NormalError:
            flash('Ha ocurrido un error inesperado al intentar dejar de seguir a los usuarios especificados, por favor revisa tu lista.','danger')
            return redirect(url_for('.unfollow_list'))

    return render_template("dejar-seguir-list.html", form=form)
