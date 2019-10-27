import os, shutil, argparse, json, time

# python code/mysimbdp-fetchdata.py --micro_batching 'Yes'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--micro_batching', type=str, default='No', help='Set "Yes" for micro-batching when size ingestion constraint not satisfied or "No" for discarting.')
    return parser.parse_args()
args = parse_args()

with open('code/config_ingestion_constraints.json', 'r') as file:
	ingestion_constraints = json.load(file)

def find_client_id(batch_filename):
    client_id_start = batch_filename.find('--client')+2
    client_id_end = batch_filename.find('.csv', client_id_start)
    return batch_filename[client_id_start:client_id_end]
	
def check_ingestion_constraints(first_batch_filename, batches_filenames):
    client_id = find_client_id(first_batch_filename)
    OK_number = sum([client_id==find_client_id(batch_filename) for batch_filename in batches_filenames])<=ingestion_constraints[client_id]['max_files_number']
    OK_size = os.path.getsize('code/client-input-directory/'+first_batch_filename)<=ingestion_constraints[client_id]['max_file_size']
    return OK_number, OK_size

def microbatching(first_batch_filename):
    client_id = find_client_id(first_batch_filename)
    max_file_size = ingestion_constraints[client_id]['max_file_size']
    microbatch = 1
    microbatch_size = 0
    microbatch_file = open('code/client-stage-directory/'+first_batch_filename.replace('.csv','')+'--microbatch'+str(microbatch)+'.csv', 'w')
    with open('code/client-input-directory/'+first_batch_filename) as file:
        for row_index, row in enumerate(file):
            if row_index==0:
                keys = row
                microbatch_file.write(keys)
                microbatch_size += len(keys)
            else:
                if microbatch_size+len(row)<=max_file_size:
                    microbatch_file.write(row)
                    microbatch_size += len(row)
                else:
                    microbatch_file.close()
                    microbatch += 1
                    microbatch_file = open('code/client-stage-directory/'+first_batch_filename.replace('.csv','')+'--microbatch'+str(microbatch)+'.csv', 'w')
                    microbatch_file.write(keys)
                    microbatch_file.write(row)
                    microbatch_size = len(keys)+len(row)
        microbatch_file.close()
    os.remove('code/client-input-directory/'+first_batch_filename)

while True:
    batches_filenames = os.listdir('code/client-input-directory')
    if len(batches_filenames)>0:
        first_batch_filename = batches_filenames[0]
        OK_number, OK_size = check_ingestion_constraints(first_batch_filename, batches_filenames)
        if OK_number and OK_size:
            shutil.move('code/client-input-directory/'+first_batch_filename, 'code/client-stage-directory/'+first_batch_filename)
        elif OK_number and not OK_size and args.micro_batching=='Yes':
            microbatching(first_batch_filename)
        else:
            # os.remove('code/client-input-directory/'+first_batch_filename)
            shutil.move('code/client-input-directory/'+first_batch_filename, 'code/client-no_stage-directory/'+first_batch_filename)
    time.sleep(7)