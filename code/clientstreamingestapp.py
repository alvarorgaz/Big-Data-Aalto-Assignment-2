import threading, pika, sys, pymongo, json, time

args = sys.argv[1]
rabbitmq_topic, client_id, server_address = args['rabbitmq_topic'], args['client_id'], args['server_address']

mongo_client = pymongo.MongoClient('mongodb+srv://alvarorgaz:XLao4jEcoIz3kFXH@big-data-a1-j25ko.gcp.mongodb.net/admin?retryWrites=true&w=majority')
database = clientmongo['google_play_store']
table = database[client_id]
    
rabbitmq_credentials = pika.PlainCredentials('user', 'CzZETuZ1giTb')
rabbitmq_parameters = pika.ConnectionParameters(args.server_address, '5672', '/', rabbitmq_credentials)
rabbitmq_connection = pika.BlockingConnection(rabbitmq_parameters)
rabbitmq_channel = rabbitmq_connection.channel()

class publish_report_ingestion(threading.Thread):
    def __init__(self, sending_time, end_ingestion, start_ingestion):
        self.sending_time, self.start_ingestion, self.end_ingestion = sending_time, start_ingestion, end_ingestion
    def run(self):
        collection_stats = database.command('collstats', client_id)
        report = {
                 'client_id':client_id,
                 'ingestion_time':self.end_ingestion-self.start_ingestion,
                 'total_time':self.end_ingestion-self.sending_time,
                 'collection_size':collection_stats['size'],
                 'collection_count':collection_stats['count'],
                 'collection_avgObjSize':collection_stats['avgObjSize']
                 }
        rabbitmq_channel.basic_publish(exchange='', routing_key='reporting', body=json.dumps(report))
        ###########database['reports'].insert(report) ###################

def callback(_, _, _, body):
    print('Received'+body.decode()) ############
    message_json = json.loads(body.decode())
    sending_time, data = message_json['sending_time'], message_json['data']
    start_ingestion = time.time()
    table.insert()
    end_ingestion = time.time()
    publish_report_ingestion(sending_time, end_ingestion, start_ingestion).start()

rabbitmq_channel.queue_declare(queue=rabbitmq_topic)
rabbitmq_channel.basic_consume(queue=rabbitmq_topic, on_message_callback=callback) ###############3, auto_ack=True)
rabbitmq_channel.start_consuming()
print('[*] Waiting for messages on topic', rabbitmq_topic, '. To exit press Ctrl+C.')