from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required
from shellmancer import db
from shellmancer.users.utils import save_picture
from shellmancer.models import SinglePlayerCampaign
from shellmancer.users.forms import UserSettingsForm

users = Blueprint('users', 'shellmancer')


@users.route('/player')
@login_required
def player_profile():
    return render_template("player.html")


@users.route('/gamemaster')
@login_required
def gamemaster_profile():
    if current_user.gamemaster.access > 0:
        campaigns = SinglePlayerCampaign.query.filter_by(gamemaster_id=current_user.gamemaster.id).all()
        return render_template("gamemaster.html", campaigns=campaigns, context=f"by {current_user.user_name}")
    else:
        flash("This user is not a gamemaster", 'info')
        return redirect(url_for('users.player_profile'))


@users.route('/gamemaster-make')
@login_required
def make_gamemaster():
    if current_user.gamemaster.access > 0:
        flash("User is already a game master", 'info')
        return redirect(url_for('users.gamemaster_profile'))
    else:
        current_user.gamemaster.access = 1
        db.session.add(current_user)
        db.session.commit()
        flash("{{current_user.email}} set to gamemaster.")
        return redirect(url_for('users.gamemaster_profile'))





@users.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = UserSettingsForm()
    if form.validate_on_submit():

        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file

        if form.email.data != current_user.email:
            current_user.is_verified = False
            flash('Your verified status is now pending verification of the new email.', 'warning')

        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.is_over_18 = form.is_over_18.data
        current_user.is_email_public = form.is_email_public.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('users.user_settings'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.is_over_18.data = current_user.is_over_18
        form.is_email_public.data = current_user.is_email_public
    return render_template('settings.html',
                           title=f"Settings for {current_user.email}",
                           form=form)
