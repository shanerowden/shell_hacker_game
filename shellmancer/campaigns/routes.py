from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from shellmancer import db
from shellmancer.models import SinglePlayerCampaign, CharacterSheet
from shellmancer.campaigns.forms import NewCampaignForm, CampaignSettingsForm

campaigns = Blueprint('campaigns', 'shellmancer')


@campaigns.route('/campaign/new', methods=['GET', 'POST'])
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
            return redirect(url_for('campaigns.campaign_settings', camp_id=campaign.id))
    return render_template("campaign_new.html",
                           form=form, title="New Campaign")


@campaigns.route('/campaign/<camp_id>/update', methods=['GET', 'POST'])
@login_required
def campaign_settings(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash('This campaign does not exist.', 'info')
        return redirect(url_for('campaigns.all_campaigns'))

    if current_user.gamemaster.id != campaign.gamemaster.id:
        return redirect(url_for('campaigns.campaign_profile', camp_id=camp_id))

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


@campaigns.route('/campaign')
def all_campaigns():
    campaigns = SinglePlayerCampaign.query.all()
    campaigns.reverse()

    return render_template('campaigns.html',
                           title="All Campaigns", campaigns=campaigns, context="ALL")



@campaigns.route('/campaign/<camp_id>')
def campaign_profile(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        return redirect(url_for('campaigns.all_campaigns'))

    characters = CharacterSheet.query.filter_by(
        campaign_id=camp_id, player_id=current_user.player.id).all()

    if len(characters) < 1:
        flash("You do not have any characters for this campaign yet. Make one!", "info")

    return render_template('campaign_profile.html',
                           title=f"Campaign | {campaign.name}", campaign=campaign, character_count=len(characters),
                           pfp=f"img/pfp/{campaign.gamemaster.user.image_file}")




@campaigns.route('/campaign/<camp_id>/delete')
def campaign_delete(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash('This campaign does not exist.', 'info')
        return redirect(url_for('campaigns.all_campaigns'))
    if current_user.id == campaign.gamemaster_id:
        db.session.delete(campaign)
        db.session.commit()
        flash("Campaign has been deleted", 'success')
        return redirect(url_for('campaigns.campaign_profile', camp_id=camp_id))
    flash("You cannot delete a campaign that does not belong to you", 'warning')
    return redirect(url_for('campaigns.campaign_profile', camp_id=camp_id))



@campaigns.route('/campaign/<camp_id>/new')
@login_required
def new_character(camp_id):
    campaign = SinglePlayerCampaign.query.get(camp_id)
    return render_template("character_new.html", campaign=campaign)




@campaigns.route('/campaign/<camp_id>/characters/')
@login_required
def campaign_characters(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash('This campaign does not exist.', 'info')
        return redirect(url_for('campaigns.all_campaigns'))


    return render_template("campaign_characters.html", characters=characters,
                           title=f"Characters for {campaign.name}", campaign=campaign)




@campaigns.route('/campaign/<camp_id>/popup')
def campaign_popup(camp_id):
    try:
        campaign = SinglePlayerCampaign.query.get(camp_id)
    except:
        flash("That campaign does not exist", "info")
        return redirect(url_for('campaigns.all_campaigns'))

    return render_template('campaign_popup.html', campaign=campaign)
