# -*- coding: utf-8 -*-
from app import db, app
from app.models import Player, Role, Scenario
from flask.ext import wtf
from flask.ext.login import login_required, login_user, logout_user, current_user
from wtforms.fields import StringField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy import and_

# Define admin login forms (for flask-login)
class AdminLoginForm(wtf.Form):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate_login(self, field):
        admin = self.get_admin()

        if admin is None:
            raise ValidationError('Invalid admin')

        if admin.password != self.password.data:
            raise ValidationError('Invalid password')

    def get_admin(self):
        # return db.session.query(Player).filter_by(login=self.login.data, role_id=2).first()
        role = db.session.query(Role).filter_by(role='admin').first()
        return db.session.query(Player).filter(and_(Player.login==self.login.data, Player.role==role)).first()


class CreateScenarioForm(wtf.Form):
    pass
    # with app.app_context():
    # name = StringField('name', validators=[DataRequired()])
    # duration = StringField('duration', validators=[DataRequired()])
    # economy_status = SelectField('economy_status', choices=[(SLOW, 'SLOW [ D ~ N({}, {}) ]'.format(MU[SLOW], SIGMA[SLOW])),
    #                                                         (NEUTRAL, 'NEUTRAL [ D ~ N({}, {}) ]'.format(MU[NEUTRAL], SIGMA[NEUTRAL])),
    #                                                         (HOT, 'HOT [ D ~ N({}, {}) ]'.format(MU[HOT], SIGMA[HOT]))])

    # order_cost = StringField('order_cost', default=100, validators=[DataRequired()])
    # selling_price_hoodie = StringField('selling_price_hoodie', default=10.0, validators=[DataRequired()])
    # selling_price_trendy = StringField('selling_price_trendy', default=15.0, validators=[DataRequired()])
    # salvage_value_hoodie = StringField('salvage_value_hoodie', default=1.0, validators=[DataRequired()])
    # salvage_value_trendy = StringField('salvage_value_trendy', default=1.0, validators=[DataRequired()])

    # # supp_BR_capacity = StringField('supp_BR_capacity', default=1000, validators=[DataRequired()])
    # # supp_CH_capacity = StringField('supp_CH_capacity', default=1200, validators=[DataRequired()])
    # # supp_EU_capacity = StringField('supp_EU_capacity', default=2000, validators=[DataRequired()])
    # # supp_US_capacity = StringField('supp_US_capacity', default=1000, validators=[DataRequired()])

    # supp_BR_production_rate = StringField('supp_BR_production_rate', default=1000, validators=[DataRequired()])
    # supp_CH_production_rate = StringField('supp_CH_production_rate', default=1000, validators=[DataRequired()])
    # supp_EU_production_rate = StringField('supp_EU_production_rate', default=1000, validators=[DataRequired()])
    # supp_US_production_rate = StringField('supp_US_production_rate', default=1000, validators=[DataRequired()])

    # supp_BR_price_hoodie = StringField('supp_BR_price_hoodie', default=1.0, validators=[DataRequired()])
    # supp_CH_price_hoodie = StringField('supp_CH_price_hoodie', default=1.0, validators=[DataRequired()])
    # supp_EU_price_hoodie = StringField('supp_EU_price_hoodie', default=1.0, validators=[DataRequired()])
    # supp_US_price_hoodie = StringField('supp_US_price_hoodie', default=1.0, validators=[DataRequired()])

    # supp_BR_price_trendy = StringField('supp_BR_price_trendy', default=2.0, validators=[DataRequired()])
    # supp_CH_price_trendy = StringField('supp_CH_price_trendy', default=2.0, validators=[DataRequired()])
    # supp_EU_price_trendy = StringField('supp_EU_price_trendy', default=2.0, validators=[DataRequired()])
    # supp_US_price_trendy = StringField('supp_US_price_trendy', default=2.0, validators=[DataRequired()])

    # supp_BR_end_capacity = StringField('supp_BR_end_capacity', default=40, validators=[DataRequired()])
    # supp_CH_end_capacity = StringField('supp_CH_end_capacity', default=45, validators=[DataRequired()])
    # supp_EU_end_capacity = StringField('supp_EU_end_capacity', default=35, validators=[DataRequired()])
    # supp_US_end_capacity = StringField('supp_US_end_capacity', default=30, validators=[DataRequired()])

    # supp_BR_cancel_penalty = StringField('supp_BR_cancel_penalty', default=0, validators=[DataRequired()])
    # supp_CH_cancel_penalty = StringField('supp_CH_cancel_penalty', default=0, validators=[DataRequired()])
    # supp_EU_cancel_penalty = StringField('supp_EU_cancel_penalty', default=0, validators=[DataRequired()])
    # supp_US_cancel_penalty = StringField('supp_US_cancel_penalty', default=0, validators=[DataRequired()])

    # # supp_BR_salvage = StringField('supp_BR_salvage', default=0.0, validators=[DataRequired()])
    # # supp_CH_salvage = StringField('supp_CH_salvage', default=0.0, validators=[DataRequired()])
    # # supp_EU_salvage = StringField('supp_EU_salvage', default=0.0, validators=[DataRequired()])
    # # supp_US_salvage = StringField('supp_US_salvage', default=0.0, validators=[DataRequired()])

    # goodwill_cost_hoodie_P1 =StringField('goodwill_cost_hoodie_P1', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P2 =StringField('goodwill_cost_hoodie_P2', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P3 =StringField('goodwill_cost_hoodie_P3', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P4 =StringField('goodwill_cost_hoodie_P4', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P5 =StringField('goodwill_cost_hoodie_P5', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P6 =StringField('goodwill_cost_hoodie_P6', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P7 =StringField('goodwill_cost_hoodie_P7', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P8 =StringField('goodwill_cost_hoodie_P8', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P9 =StringField('goodwill_cost_hoodie_P9', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P10 =StringField('goodwill_cost_hoodie_P10', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P11 =StringField('goodwill_cost_hoodie_P11', default=1.0, validators=[DataRequired()])
    # goodwill_cost_hoodie_P12 =StringField('goodwill_cost_hoodie_P12', default=1.0, validators=[DataRequired()])

    # goodwill_cost_trendy_P1 =StringField('goodwill_cost_trendy_P1', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P2 =StringField('goodwill_cost_trendy_P2', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P3 =StringField('goodwill_cost_trendy_P3', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P4 =StringField('goodwill_cost_trendy_P4', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P5 =StringField('goodwill_cost_trendy_P5', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P6 =StringField('goodwill_cost_trendy_P6', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P7 =StringField('goodwill_cost_trendy_P7', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P8 =StringField('goodwill_cost_trendy_P8', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P9 =StringField('goodwill_cost_trendy_P9', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P10 =StringField('goodwill_cost_trendy_P10', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P11 =StringField('goodwill_cost_trendy_P11', default=1.0, validators=[DataRequired()])
    # goodwill_cost_trendy_P12 =StringField('goodwill_cost_trendy_P12', default=1.0, validators=[DataRequired()])

    # # owner_id = HiddenField('owner_id', default=0) # this id must be set in the view, because current_user is not available here

    def validate_scenario(self):
        pass

