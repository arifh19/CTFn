from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint
from CTFd.utils import admins_only, is_admin, cache
from CTFd.models import db, Teams, Solves, Awards, Challenges, WrongKeys, Keys, Tags, Files, Tracking, Pages, Config, Hints, Unlocks, DatabaseError, Contests
from CTFd.plugins.keys import get_key_class, KEY_CLASSES
from CTFd.plugins.challenges import get_chal_class, CHALLENGE_CLASSES

from CTFd import utils

from datetime import datetime
import pytz
import os

admin_contests = Blueprint('admin_contests', __name__)


@admin_contests.route('/admin/contests', methods=['POST', 'GET'])
@admins_only
def admin_contests_board():
    if request.method == 'POST':
        contests = Contests.query.add_columns('id', 'slug', 'name').order_by(Contests.id).all()

        json_data = {'contests': []}
        for x in contests:
            json_data['contests'].append({
                'id': x.id,
                'slug': x.slug,
                'name': x.name,
            })

        db.session.close()
        return jsonify(json_data)
    else:
        return render_template('admin/contests.html')

@admin_contests.route('/admin/contest/new', methods=['POST', 'GET'])
@admins_only
def admin_create_contests():
    if request.method == 'POST':
        # Create contest

        start_time = datetime.strptime(request.form['starttime'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['starttime'], '%Y-%m-%dT%H:%M')

        start_time = pytz.timezone(request.form['timezone']).localize(start_time).astimezone(pytz.utc)
        end_time = pytz.timezone(request.form['timezone']).localize(end_time).astimezone(pytz.utc)

        contest = Contests(request.form['slug'], request.form['name'], request.form['description'], start_time, end_time)

        db.session.add(contest)
        db.session.flush()
        db.session.commit()
        db.session.close()

        return redirect(url_for('admin_contests.admin_contests_board'))
    else:
        return render_template('admin/contests/create.html')

@admin_contests.route('/admin/contest/<int:contestid>', methods=['POST', 'GET'])
@admins_only
def admin_update_contests(contestid):
    if request.method == 'POST':
        tz = pytz.timezone(request.form['timezone'])

        contest = Contests.query.filter_by(id=contestid).first_or_404()
        contest.name = request.form['name']
        contest.slug = request.form['slug']
        contest.description = request.form['description']
        contest.starttime = tz.localize(datetime.strptime(request.form['starttime'], '%Y-%m-%dT%H:%M')).astimezone(pytz.utc).replace(tzinfo=None)
        contest.endtime = tz.localize(datetime.strptime(request.form['endtime'], '%Y-%m-%dT%H:%M')).astimezone(pytz.utc).replace(tzinfo=None)

        db.session.add(contest)
        db.session.commit()
        db.session.close()

        return redirect(url_for('admin_contests.admin_contests_board'))
    else:
        contest = Contests.query.filter_by(id=contestid).first()
        contest_dict = vars(contest)
        contest_dict.pop('_sa_instance_state', None)
        return render_template('admin/contests/update.html', contest=contest_dict)
