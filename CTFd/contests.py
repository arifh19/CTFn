from flask import render_template, request, redirect, jsonify, url_for, session, Blueprint
from sqlalchemy.sql import or_, and_

from CTFd.models import db, Challenges, Files, Solves, WrongKeys, Keys, Tags, Teams, Awards, Hints, Unlocks, Contests
from CTFd import utils

contests = Blueprint('contests', __name__)

@contests.route('/contests', methods=['GET'])
def challenges_view():
    if utils.user_can_view_challenges():  # Do we allow unauthenticated users?
        contests = Contests.query.all()
        contests_dict = []

        for x in contests:
            c = vars(x)
            c.pop('_sa_instance_state', None)
            contests_dict.append(c)

        return render_template('contests.html', contests=contests_dict)
    else:
        return redirect(url_for('auth.login', next='challenges'))
