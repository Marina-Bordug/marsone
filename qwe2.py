import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                                    'end_date', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'description']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished'],
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['PUT'])
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    jobs_data = request.json
    jobs.team_leader = jobs_data.get("team_leader", jobs.team_leader)
    jobs.job = jobs_data.get("job", jobs.job)
    jobs.work_size = jobs_data.get("work_size", jobs.work_size)
    jobs.collaborators = jobs_data.get("collaborators", jobs.collaborators)
    jobs.start_date = jobs_data.get("start_date", jobs.start_date)
    jobs.end_date = jobs_data.get("end_date", jobs.end_date)
    jobs.is_finished = jobs_data.get("is_finished", jobs.is_finished)

    db_sess.commit()

    return jsonify({'id': jobs.id, 'team_leader': jobs.team_leader, 'job': jobs.job, 'work_size': jobs.work_size,
                    'collaborators': jobs.collaborators, 'start_date': jobs.start_date, 'end_date': jobs.end_date,
                    'is_finished': jobs.is_finished})


