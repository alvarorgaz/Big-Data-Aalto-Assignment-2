import requests, argparse

# python code/client_to_mysimbdp-daas.py --client_id client1 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client1-googleplaystore1.csv & python code/client_to_mysimbdp-daas.py --client_id client1 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client1-googleplaystore2.csv & python code/client_to_mysimbdp-daas.py --client_id client1 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client1-googleplaystore3.csv & python code/client_to_mysimbdp-daas.py --client_id client2 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client2-googleplaystore_user_reviews1.csv & python code/client_to_mysimbdp-daas.py --client_id client2 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client2-googleplaystore_user_reviews2.csv & python code/client_to_mysimbdp-daas.py --client_id client2 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client2-googleplaystore_user_reviews3.csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client_id', type=str, help='Set the client ID.')
    parser.add_argument('--ingestion_mode', type=str, default='batch', help='Set the ingestion mode as "batch" or "nearrealtime".')
    parser.add_argument('--server_address', type=str, default='http://35.228.191.152/')
    parser.add_argument('--dataset_path', type=str, help='Set the path of the dataset to ingest including ".csv".')
    return parser.parse_args()
args = parse_args()

server_address = args.server_address+args.ingestion_mode+'/ingestion'

if args.ingestion_mode=='batch':
    request = requests.post(server_address, files={'client_id':args.client_id,'file':open(args.dataset_path)})
    print('Request status:', request.reason)

elif args.ingestion_mode=='nearrealtime':
    with open(args.dataset_path) as file:
        for row_index, row in enumerate(file):
            if row_index==0:
                keys = row.replace('\n','').split(',')
            else:
                request = requests.post(server_address, json={'client_id':args.client_id,'row_id':str(row_index),'data':dict(zip(keys,row.replace('\n','').split(',')))})
                print('Request status:', request.reason)