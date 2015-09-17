# -*- coding: utf-8 -*-

from app import db
from app.models import Scenario, ScenarioCode
from app.game_constants import *
from random import randint

def set_scenario_status(scenario_id, status=""):
    """
    Set the status of the given scenario
    :param scenario_code: code of the scenario
    :param status: new status
    :return:
    """
    if status in SCENARIO_STATUSES:
        scenario = Scenario.query.get(scenario_id)
        if scenario:
            scenario.status = status
            db.session.add(scenario)
            db.session.commit()
            return True
        else:
            raise ValueError('Scenario with code {} does not exist'.format(scenario_code))
    else:
        raise ValueError('Status {} is not a valid one'.format(status))


def get_new_scenario_code():
    """
    Used when creating a new scenario, check uniqueness/save from/on DB
    :return: returns a unique scenario code
    """
    new_code = randint(100, 999)

    while True:
        code = db.session.query(ScenarioCode).filter_by(code=new_code).first()
        if not code:
            new_scenario_code = ScenarioCode()
            new_scenario_code.code = new_code
            db.session.add(new_scenario_code)
            db.session.commit()
            return new_code
        else:
            new_code += 1
            if new_code > 999:
                new_code = 100
