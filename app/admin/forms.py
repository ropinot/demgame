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
    # TODO: add spot cost, spot LT, spot min lot size, spot yield
    name = StringField('name', validators=[DataRequired()])
    # duration = StringField('duration', default=25, validators=[DataRequired()])
    frozen_horizon = StringField('frozen_horizon', default=2, validators=[DataRequired()])
    leadtime = StringField('leadtime', default=1, validators=[DataRequired()])
    forecast_horizon = StringField('forecast_horizon', default=1, validators=[DataRequired()])

    product_cost = StringField('product_cost', default=1, validators=[DataRequired()])
    stock_cost = StringField('stock_cost', default=1, validators=[DataRequired()])
    lostsale_cost = StringField('lostsale_cost', default=1, validators=[DataRequired()])
    order_cost = StringField('order_cost', default=10, validators=[DataRequired()])

    spot_cost = StringField('spot_cost', default=2., validators=[DataRequired()])
    spot_leadtime = StringField('spot_leadtime', default=1, validators=[DataRequired()])
    spot_min_lotsize = StringField('spot_min_lotsize', default=0, validators=[DataRequired()])
    spot_yield = StringField('spot_yield', default=100., validators=[DataRequired()])

    demand_profile_id = SelectField('demand_profile_id', coerce=int)

    # owner_id = HiddenField('owner_id', default=0) # this id must be set in the view, because current_user is not available here

    def validate_scenario(self):
        pass

