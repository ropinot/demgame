# -*- coding: utf-8 -*-
from __future__ import division
from flask import redirect, url_for
from flask.ext.login import current_user
from app import app, db
from app.models import Scenario, ScenarioCounter
from app.game_constants import *
from app.admin.admin_functions import set_scenario_status
from functools import wraps
import json
import sys

def admin_required(func):
    """
    Decorator for limiting the access to the adminviews to admins only
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if current_user.get_role() == ADMIN:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('player_home_view'))
    return func_wrapper


def get_scenario_id(scenario_code):
    return db.session.query(Scenario.id).filter_by(code=scenario_code).first()[0]
