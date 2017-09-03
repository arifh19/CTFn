from flask import render_template, request, redirect, jsonify, url_for, session, Blueprint
from sqlalchemy.sql import or_, and_

from CTFd.models import db, Challenges, Files, Solves, WrongKeys, Keys, Tags, Teams, Awards, Hints, Unlocks, Contests, Participations
from CTFd import utils

contests = Blueprint('contests', __name__)

@contests.route('/contests', methods=['GET'])
def contests_view():
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

@contests.route('/contest/<contest_slug>/participate/confirm', methods=['GET'])
def contest_participate_confirm(contest_slug):
    if utils.user_can_view_challenges():  # Do we allow unauthenticated users?
        contest = Contests.query.filter_by(slug=contest_slug).first()
        if utils.is_participated(contest):
            return redirect('/contest/' + contest_slug + '/challenges')

        if contest.protected:
            if request.args.get('password') == contest.password:
                participation = Participations(session.get('id'), contest.id)
                db.session.add(participation)
                db.session.commit()
                db.session.close()
                return redirect('/contest/' + contest_slug + '/challenges')
            else:
                return redirect('/contest/' + contest_slug + '/participate')

        else:
            participation = Participations(session.get('id'), contest.id)
            db.session.add(participation)
            db.session.commit()
            db.session.close()

            return redirect('/contest/' + contest_slug + '/challenges')
    else:
        return redirect(url_for('auth.login', next='challenges'))

@contests.route('/contest/<contest_slug>/participate', methods=['GET'])
def contest_participate(contest_slug):
    if utils.user_can_view_challenges():  # Do we allow unauthenticated users?
        contest = Contests.query.filter_by(slug=contest_slug).first()
        if utils.is_participated(contest):
            return redirect('/contest/' + contest_slug + '/challenges')

        contest_dict = vars(contest)
        contest_dict.pop('_sa_instance_state', None)

        return render_template('participating.html', contest=contest_dict)
    else:
        return redirect(url_for('auth.login', next='challenges'))

