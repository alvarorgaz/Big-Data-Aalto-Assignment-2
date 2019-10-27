from flask import Flask, request
from flask_restplus import Resource, Api
from datetime import datetime

# python code/mysimbdp-daas.py

flaskapp = Flask(__name__)
app = Api(app=flaskapp)
app_batch = app.namespace('batch', description='APIs concerning full datasets to client-input-directory (batch ingestion).')
app_nearrealtime = app.namespace('nearrealtime', description='APIs concerning message to databroker (near-realtime ingestion).')

@app_batch.route('/ingestion', methods=['POST'])
class ingestion(Resource):
    def post(self):
        client_id = request.files['client_id'].read().decode("utf-8")
        filename = 'code/client-input-directory/'+str(datetime.now()).replace(':', '-')+'--'+client_id+'.csv'
        request.files['file'].save(filename)
        return ''

@app_nearrealtime.route('/ingestion', methods=['POST'])
class ingestion(Resource):
    def post(self):
        message = message['data']
        message_name = str(datetime.now()).replace(':', '-')+'--'+request.json['client_id']+'--row'+request.json['row_id']+'.json'
        print('\n')
        print(message_name)
        print(message)
        # send to broker
        return ''
		
flaskapp.run()# host='0.0.0.0', port=80
