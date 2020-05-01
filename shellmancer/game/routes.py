from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from shellmancer import db, ph
from shellmancer.models import SinglePlayerCampaign, CharacterSheet
from shellmancer.game.forms import NewCampaignForm, CampaignSettingsForm
from shellmancer.auth.forms import RegisterForm
from shellmancer.models import UserAccount
from shellmancer.auth.utils import send_verify_email


game = Blueprint('game', 'shellmancer')


@game.route('/campaign/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    if not current_user.gamemaster.access > 0:
        return redirect(url_for('users.player_profile'))
    else:
        form = NewCampaignForm()
        if form.validate_on_submit():
            campaign = SinglePlayerCampaign(name=form.title.data,
                                            descrip=form.descrip.data,
                                            gamemaster_id=current_user.gamemaster.id)
            db.session.add(campaign)
            db.session.commit()
            return redirect(url_for('game.campaign_settings', camp_id=campaign.id))
    return render_template("campaign_new.html",
                           form=form, title="New Campaign")


@game.route('/campaign/<camp_id>/update', methods=['GET', 'POST'])
@login_required
def campaign_settings(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash('This campaign does not exist.', 'info')
        return redirect(url_for('game.all_campaigns'))

    if current_user.gamemaster.id != campaign.gamemaster.id:
        return redirect(url_for('game.campaign_profile', camp_id=camp_id))

    else:
        form = CampaignSettingsForm()
        if form.validate_on_submit():
            campaign.name = form.title.data
            campaign.descrip = form.descrip.data
            campaign.intro_text = form.intro_text.data
            campaign.attr_a_name = form.attr_a_name.data
            campaign.attr_b_name = form.attr_b_name.data
            campaign.attr_c_name = form.attr_c_name.data
            campaign.attr_a_descrip = form.attr_a_descrip.data
            campaign.attr_b_descrip = form.attr_b_descrip.data
            campaign.attr_c_descrip = form.attr_c_descrip.data
            campaign.has_adult_content = form.has_adult_content.data
            db.session.commit()
        elif request.method == 'GET':
            form.title.data = campaign.name
            form.descrip.data = campaign.descrip
            form.intro_text.data = campaign.intro_text
            form.attr_a_name.data = campaign.attr_a_name
            form.attr_b_name.data = campaign.attr_b_name
            form.attr_c_name.data = campaign.attr_c_name
            form.attr_a_descrip.data = campaign.attr_a_descrip
            form.attr_b_descrip.data = campaign.attr_b_descrip
            form.attr_c_descrip.data = campaign.attr_c_descrip
    return render_template("campaign_settings.html", form=form, campaign=campaign,
                           title=f"Settings '{campaign.name}'")


@game.route('/campaign')
@login_required
def all_campaigns():
    # Temporary Redirect Away From Campaign List
    if True:
        flash("For now, the campaign directory redirects here. It's the only campaign afterall.", "secondary")
        return redirect(url_for("game.campaign_profile", camp_id=1))

    # campaigns = SinglePlayerCampaign.query.all()
    # campaigns.reverse()
    # return render_template('campaigns.html',
    #                        title="All Campaigns", campaigns=campaigns, context="ALL")



@game.route('/campaign/<camp_id>')
@login_required
def campaign_profile(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        return redirect(url_for('game.all_campaigns'))

    characters = CharacterSheet.query.filter_by(
        campaign_id=camp_id, player_id=current_user.player.id).all()

    if len(characters) < 1:
        flash("You do not have any characters for this campaign yet. Make one!", "info")

    return render_template('campaign_profile.html',
                           title=f"Campaign | {campaign.name}", campaign=campaign, character_count=len(characters),
                           pfp=f"img/pfp/{campaign.gamemaster.user.image_file}")




@game.route('/campaign/<camp_id>/delete')
@login_required
def campaign_delete(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash('This campaign does not exist.', 'info')
        return redirect(url_for('game.all_campaigns'))
    if current_user.id == campaign.gamemaster_id:
        db.session.delete(campaign)
        db.session.commit()
        flash("Campaign has been deleted", 'success')
        return redirect(url_for('game.campaign_profile', camp_id=camp_id))
    flash("You cannot delete a campaign that does not belong to you", 'warning')
    return redirect(url_for('game.campaign_profile', camp_id=camp_id))



@game.route('/campaign/<camp_id>/new', methods=['GET', 'POST'])
def new_character(camp_id):
    campaign = SinglePlayerCampaign.query.get(camp_id)

    if not campaign:
        return redirect(url_for("game.all_campaigns"))

    if not current_user.is_authenticated:
        flash("You are viewing a limited preview of this site without an account. You'll need one to save.", "danger")
        form = RegisterForm()

        if form.validate_on_submit():
            hashed_pw = ph.hash(form.password.data)
            user = UserAccount(email=form.email.data, password=hashed_pw)

            db.session.add(user)
            db.session.commit()

            send_verify_email(user)

            flash(f"Account created for {form.email.data}"
                  + "Check your email to verify account for full functionality. You may login now.", 'success')
            return redirect(url_for('auth.login'))
    else:
        form = None
    # flash("You will lose any progress if you navigate away from this page without submitting.", "danger")

    return render_template("character_new.html", campaign=campaign, form=form)




@game.route('/campaign/<camp_id>/characters/')
@login_required
def campaign_characters(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash('This campaign does not exist.', 'info')
        return redirect(url_for('game.all_campaigns'))


    return render_template("campaign_characters.html", characters=characters,
                           title=f"Characters for {campaign.name}", campaign=campaign)




@game.route('/campaign/<camp_id>/popup')
def campaign_popup(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash("That campaign does not exist", "info")
        return redirect(url_for('game.all_campaigns'))

    return render_template('campaign_popup.html', campaign=campaign)

