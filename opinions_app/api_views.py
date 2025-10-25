from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import Opinion
from .views import get_random_opinion


def validate_update_data(data):
    if data is None:
        raise InvalidAPIUsage('В запросе ничего не передано!')
    if ('text' in data) and (Opinion.query.filter_by(text=data['text']).first() is not None):
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')


def validate_create_data(data):
    validate_update_data(data)
    if 'title' not in data or 'text' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    return True


def get_opinion_or_404(id):
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Такого мнения не существует!', 404)
    return opinion


@app.route('/api/opinions/<int:id>/', methods=['GET', 'PATCH'])
def get_update_opinion(id):
    opinion = get_opinion_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        validate_update_data(data)
        opinion.title = data.get('title', opinion.title)
        opinion.text = data.get('text', opinion.text)
        opinion.source = data.get('source', opinion.source)
        opinion.added_by = data.get('added_by', opinion.added_by)
        db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = get_opinion_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    data = request.get_json(silent=True)
    validate_create_data(data)
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random():
    opinion = get_random_opinion()
    if opinion is None:
        raise InvalidAPIUsage('В базе данных нет мнений', 404)
    return jsonify({'opinion': opinion.to_dict()}), 200
