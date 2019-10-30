import pika, argparse, threading, time, random, json, ctypes, pandas

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client_id', type=str, help='Set the client ID.')
    parser.add_argument('--dataset_path', type=str, help='Set the path of the dataset to ingest including the extension.')
    parser.add_argument('--server_address', type=str, default='http://35.228.167.103/')
    return parser.parse_args()
args = parse_args()

def find_extension(filename):
    return filename.split('.')[-1]
args.file_extension = find_extension(args.dataset_path)

rabbitmq_topics_client_id = []
rabbitmq_credentials = pika.PlainCredentials('user', 'CzZETuZ1giTb')
rabbitmq_parameters = pika.ConnectionParameters(args.server_address, '5672', '/', rabbitmq_credentials)
rabbitmq_connection = pika.BlockingConnection(rabbitmq_parameters)
rabbitmq_channel = rabbitmq_connection.channel()

class get_available_rabbitmq_topics_client_id(threading.Thread):
    def __init__(self, client_id):
        self.client_id = client_id    
    def run(self):
        def callback(_, _, _, body):
            global rabbitmq_topics_client_id
            print(body) #################################################3 DELETE
            rabbitmq_topics_client_id = body.decode().split(',')
        rabbitmq_channel.basic_consume(queue='rabbitmq_topics_'+self.client_id, on_message_callback=callback) #################, auto_ack=True)
        rabbitmq_channel.start_consuming()    
    def get_id(self):
       if hasattr(self, '_thread_id'):
           return self._thread_id
       for id, thread in threading._active.items():
           if thread is self:
               return id    
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))

available_rabbitmq_topics_client_id = get_available_rabbitmq_topics(args.client_id)
available_rabbitmq_topics_client_id.start()
while not len(rabbitmq_topics_client_id)>0:
    time.sleep(1)

if args.file_extension=='csv':
    data = pandas.read_csv(args.dataset_path)
elif args.file_extension=='json':
    data = pandas.read_json(args.dataset_path)

start = time.time()
for row in data.index:
    row_to_ingest_json = data.loc[[row],].to_dict(orient='records')[0]
    message_json = {'data':row_to_ingest_json,'sending_time':time.time()}
    rabbitmq_channel.basic_publish(exchange='', routing_key=random.choice(rabbitmq_topics_client_id), body=json.dumps(message_json))
print('All data sent to message broker in', time.time()-start, 'seconds.')

rabbitmq_connection.close()
available_rabbitmq_topics_client_id.raise_exception() ###########################33