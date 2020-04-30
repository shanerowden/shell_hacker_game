from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from shellmancer.models import SinglePlayerCampaign

main = Blueprint('main', 'shellmancer')

@main.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return redirect(url_for('game.campaign_profile', camp_id=1))
    # return render_template('index.html')

@main.route('/docs')
def docs():
    return render_template("docs.html")

@main.route('/test')
def testing():
    campaign = SinglePlayerCampaign.query.get(2)
    return render_template("testing.html", campaign=campaign)



