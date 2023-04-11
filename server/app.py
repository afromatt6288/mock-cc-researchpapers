#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
# from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'

class Index(Resource):
    def get(self):
        response = make_response('<h1>Code challenge</h1>', 200)
        return response
    
api.add_resource(Index, '/')

# @app.route('/research')
# def restaurants():

#     pass

class Researches(Resource):
    def get(self):
        response_dict_list = []
        for n in Research.query.all():
            response_dict_list.append(n.to_dict(only=('id', 'topic', 'year', 'page_count')))
        response = make_response(response_dict_list, 200)
        return response

api.add_resource(Researches, '/research')

class ResearchById(Resource):
    def get(self, id):
        res = Research.query.filter(Research.id == id).first()
        if res:
            response_dict = res.to_dict()
            response = make_response(jsonify(response_dict, 200))
            return response
        return make_response(jsonify({"error": "Research Paper not found"}), 404)
    
    def delete(self, id):
        record = Research.query.filter(Research.id == id).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Record successfully deleted"}
            return make_response(response_dict, 200)
        return make_response(jsonify({"error": "Research Paper not found"}), 404)
        
api.add_resource(ResearchById, '/research/<int:id>')

class Authors(Resource):
    def get(self):
        return make_response([n.to_dict(only=('id', 'name', 'field_of_study')) for n in Author.query.all()], 200)

api.add_resource(Authors, '/authors')


class ResearchAuthors(Resource):
    # def get(self):
    #     response_dict_list = []
    #     for n in ResearchAuthor.query.all():
    #         response_dict_list.append(n.to_dict())
    #     response = make_response(response_dict_list, 200)
    #     return response
	# ## OR ##
    def get(self):
        return make_response([n.to_dict() for n in ResearchAuthor.query.all()], 200)

    def post(self):
        try:
            new_record = ResearchAuthor(
                author_id=int(request.form.get('author_id')), 
                research_id=int(request.form.get('research_id')),
                )
            db.session.add(new_record)
            db.session.commit()
        except Exception as e:
            return make_response({"errors": [e.__str__()]}, 422)
        response = make_response(jsonify(new_record.to_dict()['author']), 201)
        return response 

api.add_resource(ResearchAuthors, '/research_authors')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
