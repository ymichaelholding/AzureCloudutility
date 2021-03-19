import configparser
import os
import glob
from azure.storage.blob import ContainerClient
import logging

config = configparser.ConfigParser()
configfile = r'\PycharmProjects\Python\lib\Azure_config.ini'
properties = config.read(configfile)
log_file=r"\PycharmProjects\Python\lib\app.log"

logging.basicConfig(filename=log_file, filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Admin logged in')

def load_azure_config():
    credentials = config['AZURE']['credentials']
    container = config['AZURE']['container']
    inbound_folder = config['AZURE']['inbound_folder']
    return credentials,container,inbound_folder

def get_input_files(inbound_folder):
     with os.scandir(inbound_folder) as files:
           for file in files:
               if file.is_file() and not file.name.startswith('.'):
                   yield file

def file_upload(files,connections_string,containter_name):
    container_client = ContainerClient.from_connection_string(connections_string,containter_name)
    print(type(container_client))
    for file in files:
        print(file)
        logging.info('copying the files to Azure cloud inprogress')
        blob_client=container_client.get_blob_client(file.name)
        print(type(blob_client))
        logging.info('files names' + file.name)
        with open(file.path,"rb") as data:
              print(data)
              #blob_client.upload_blob(data)
    return 0

def main():
    credentials, container, inbound_folder = load_azure_config()
    logging.info('credentials' + credentials)
    logging.info('container' + container)
    logging.info('inbound_folder' + inbound_folder)
    list_of_files = get_input_files(inbound_folder)
    file_upload(list_of_files, credentials, container)
    logging.info('copying the files to Azure cloud Completed')
    return True

if __name__ == "__main__":
    print(main())
