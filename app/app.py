from bson import json_util, ObjectId
from datetime import datetime
from flask import Flask, request

from app.helpers import mongo_client

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))


@app.route('/engagements/<engagement_id>/interactions')
def interactions(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    query = {'$and': [{'engagementId': engagement_object_id}]}

    if start_date is not None:
        try:
            formatted_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            formatted_date = datetime.strptime(start_date, '%Y-%m-%d')
        query['$and'].append({'interactionDate': {'$gte': formatted_date}})

    if end_date is not None:
        try:
            formatted_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            formatted_date = datetime.strptime(end_date, '%Y-%m-%d')
        query['$and'].append({'interactionDate': {'$gte': formatted_date}})

    return json_util.dumps(db.interactions.find(query))


@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))
