import json
import os
from google.cloud import bigquery, storage
from tools.logger_client import gc_logger

with open('config.json') as f:
    data = json.load(f)
    print(data)



mail_setting = {
  "MAIL_SERVER" : 'smtp.gmail.com',
  "MAIL_USE_TLS" : False,
  "MAIL_USE_SSL" : True,
  "MAIL_PORT" : 465, 
  "MAIL_USERNAME" : "olivier.randavel@m13h.com",
  "MAIL_PASSWORD" : "hhdnrxjkdbjppkui"
}

environment = data['environment']
local = data['local']

if data['local'] == 1:
    if data['environment'] == 'PROD':
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "setup/credentials/key_prod.json"

if environment == 'PROD':
    project = 'm13h-sandbox'
    service_account = ''
    root_domain = ''

concurrency = 10

queue = 'master-import'
location = 'europe-west1'
print(project)
bq_client = bigquery.Client(project=project)