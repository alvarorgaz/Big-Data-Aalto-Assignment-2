import requests, argparse

# python code/client_file_to_mysimbdp-daas.py --client_id client1 --server_address http://127.0.0.1:5000/ --dataset_path data/client1-googleplaystore1.json
# & python code/client_to_mysimbdp-daas.py --client_id client1 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client1-googleplaystore2.csv & python code/client_to_mysimbdp-daas.py --client_id client1 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client1-googleplaystore3.csv & python code/client_to_mysimbdp-daas.py --client_id client2 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client2-googleplaystore_user_reviews1.csv & python code/client_to_mysimbdp-daas.py --client_id client2 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client2-googleplaystore_user_reviews2.csv & python code/client_to_mysimbdp-daas.py --client_id client2 --ingestion_mode "batch" --server_address http://127.0.0.1:5000/ --dataset_path data/client2-googleplaystore_user_reviews3.csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client_id', type=str, help='Set the client ID.')
    parser.add_argument('--server_address', type=str, default='http://35.228.191.152/')
    parser.add_argument('--dataset_path', type=str, help='Set the path of the dataset to ingest including ".csv".')
    return parser.parse_args()
args = parse_args()

server_address = args.server_address+'batch/ingestion'
request = requests.post(server_address, files={'client_id':args.client_id,'file':open(args.dataset_path)})
print('Request status:', request.reason)