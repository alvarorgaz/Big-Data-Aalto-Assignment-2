import os, importlib, time
import pandas as pd

# python code\mysimbdp-batchingestmanager.py >> logs/batch_ingestion.log

def find_client_id(batch_filename):
    client_id_start = batch_filename.find('--client')+2
    index_microbatch = batch_filename.find('--microbatch', client_id_start)
    client_id_end = batch_filename.find('.csv', client_id_start) if index_microbatch==-1 else index_microbatch
    return batch_filename[client_id_start:client_id_end]

while True:
    batches_filenames = os.listdir('code/client-stage-directory')
    if len(batches_filenames)>0:
        first_batch_filename = batches_filenames[0]
        client_id = find_client_id(first_batch_filename)
        client_app = importlib.import_module('clientbatchingestapp--'+client_id)
        report = client_app.ingestion('code/client-stage-directory/'+first_batch_filename)
        print('For file "'+first_batch_filename+'" the ingestion report is:\n', report, '\n')
        os.remove('code/client-stage-directory/'+first_batch_filename)
    time.sleep(7)