from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

campaign_title = "Title of Campaign"
campaign_descrip = "Campaign Description"



class NewCampaignForm(FlaskForm):
    title = StringField(campaign_title,
                        validators=[DataRequired()],
                        render_kw={'placeholder': campaign_title})
    descrip = TextAreaField(campaign_descrip,
                            validators=[DataRequired(),
                                        Length(min=50, max=250)],
                            render_kw={'placeholder': campaign_descrip})
    submit = SubmitField('Create')


intro_text_label = "Introduce Your Campaign to the Players"
attr_name_label = "Name for Attribute "
attr_descrip_label = "Describe how this attribute affects the game to the player."

class CampaignSettingsForm(FlaskForm):
    title = StringField(campaign_title,
                        validators=[DataRequired()],
                        render_kw={'placeholder': campaign_title})
    descrip = StringField(campaign_descrip,
                          validators=[DataRequired(),
                                      Length(min=50, max=250)],
                          render_kw={'placeholder': campaign_descrip})
    intro_text = TextAreaField(intro_text_label,
                               validators=[DataRequired(),
                                           Length(min=250, max=2800)],
                               render_kw={'placeholder': intro_text_label})
    attr_a_name = StringField(attr_name_label + "A",
                              validators=[DataRequired(),
                                          Length(min=3, max=25)],
                              render_kw={'placeholder': attr_name_label + "A"})
    attr_b_name = StringField(attr_name_label + "B",
                              validators=[DataRequired(),
                                          Length(min=3, max=25)],
                              render_kw={'placeholder': attr_name_label + "B"})
    attr_c_name = StringField(attr_name_label + "C",
                              validators=[DataRequired(),
                                          Length(min=3, max=25)],
                              render_kw={'placeholder': attr_name_label + "C"})
    attr_a_descrip = StringField(attr_descrip_label,
                                 validators=[DataRequired(),
                                             Length(min=100, max=250)],
                                 render_kw={'placeholder': attr_descrip_label})
    attr_b_descrip = StringField(attr_descrip_label,
                                 validators=[DataRequired(),
                                             Length(min=100, max=250)],
                                 render_kw={'placeholder': attr_descrip_label})
    attr_c_descrip = StringField(attr_descrip_label,
                                 validators=[DataRequired(),
                                             Length(min=100, max=250)],
                                 render_kw={'placeholder': attr_descrip_label})
    has_adult_content = BooleanField("Should players of this campaign not be minors?")
    submit = SubmitField('Update Campaign')
