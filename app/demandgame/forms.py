# -*- coding: utf-8 -*-
from app import db, app
from flask.ext import wtf
from flask.ext.login import login_required, login_user, logout_user, current_user
from wtforms.fields import StringField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy import and_

class OrderForm(wtf.Form):
    qty = StringField('qty', default=0, validators=[DataRequired()])

    def validate_order(self):
        pass

