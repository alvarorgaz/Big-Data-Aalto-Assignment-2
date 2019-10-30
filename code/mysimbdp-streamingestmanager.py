import pika, json, time, subprocess, threading, os, signal

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_address', type=str, default='http://35.228.167.103/')
    return parser.parse_args()
args = parse_args()

rabbitmq_credentials = pika.PlainCredentials('user', 'CzZETuZ1giTb')
rabbitmq_parameters = pika.ConnectionParameters(args.server_address, '5672', '/', rabbitmq_credentials)
rabbitmq_connection = pika.BlockingConnection(rabbitmq_parameters)
rabbitmq_channel = rabbitmq_connection.channel()

available_rabbitmq_topics = {'client1':[],'client2':[]}
active_apps = {'client1':[],'client2':[]}

class publish_available_rabbitmq_topics_client_id(threading.Thread):
    def __init__(self):
        pass
    def run(self):
        while True:
            for client_id in available_rabbitmq_topics.keys():
                rabbitmq_channel.queue_declare(queue='rabbitmq_topics_'+client_id)
                rabbitmq_channel.basic_publish(exchange='', routing_key='rabbitmq_topics_'+client_id, body=','.join(available_rabbitmq_topics[client_id]))
            time.sleep(20)

publish_available_rabbitmq_topics_client_id().start()

class get_report_ingestion(threading.Thread):
    def __init__(self):
        pass
    def run(self):
        def callback(_, _, _, body):
            global active_apps, available_rabbitmq_topics
            report = json.loads(body.decode())
            if report['total_time']>10:
                client_id = report['client_id']
                rabbitmq_topic = client_id+'_app'+str(len(available_rabbitmq_topics[client_id]))
                print('Starting new app and RabbitMQ topic for', client_id)                
                arguments = {'rabbitmq_topic':rabbitmq_topic,'client_id':client_id,'server_address':args.server_address}
                app = subprocess.Popen(['python', 'clientstreamingestapp.py', arguments])
                available_rabbitmq_topics[client_id].append(rabbitmq_topic)
                active_apps[client_id].append(app)
            if report['total_time']<=10 and len(available_rabbitmq_topics[client_id])>1:
                for app_index in range(active_apps[client_id]):
                    if app_index==0:
                        continue
                    os.killpg(os.getpgid(active_apps[client_id][app_index].pid), signal.SIGTERM)
                active_apps[client_id] = [active_apps[client_id][0]]
                available_rabbitmq_topics = [available_rabbitmq_topics[0]]
        channel.queue_declare(queue='reporting')
        channel.basic_consume(queue='reporting', on_message_callback=callback) ##############, auto_ack=True)
        channel.start_consuming()

get_report_ingestion().start()

for client_id in available_rabbitmq_topics.keys():
    rabbitmq_topic = client_id+'_app'+str(len(available_rabbitmq_topics[client_id]))
    arguments = {'rabbitmq_topic':rabbitmq_topic,'client_id':client_id,'server_address':args.server_address}
    app = subprocess.Popen(['python', 'clientstreamingestapp.py', arguments])
    available_rabbitmq_topics[client_id].append(rabbitmq_topic)
    active_apps[client_id].append(app)