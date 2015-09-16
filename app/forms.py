# -*- coding: utf-8 -*-
from app import db
from models import Player
from flask.ext import wtf
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError


# Define login and registration forms (for flask-login)
class LoginForm(wtf.Form):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate_login(self, field):
        player = self.get_player()

        if player is None:
            raise ValidationError('Invalid user')

        if player.password != self.password.data:
            raise ValidationError('Invalid password')

    def get_player(self):
        return db.session.query(Player).filter_by(login=self.login.data).first()


class RegistrationForm(wtf.Form):
    login = StringField(validators=[DataRequired()])
    # email = StringField()
    password = PasswordField(validators=[DataRequired()])

    def validate_login(self, field):
        if db.session.query(Player).filter_by(login=self.login.data).count() > 0:
            raise ValidationError('Duplicate username')


class NewGameForm(wtf.Form):
    code = StringField(validators=[DataRequired()])

    def validate_code(self, field):
        pass

