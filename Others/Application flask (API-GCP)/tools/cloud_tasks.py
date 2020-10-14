
from google.cloud import tasks_v2beta3, tasks_v2
from google.protobuf import timestamp_pb2
import datetime
import os
import time

from apps import root_domain, project, queue, location, service_account

def push_task(task_name, in_seconds=1, payload=None, queue=queue, concurrent_dispatch=100):

    url = root_domain+'/'+task_name

    client = tasks_v2beta3.CloudTasksClient()

    parent = client.queue_path(project, location, queue)

    task = {
            'http_request': {  
                'http_method': 'POST',
                'url': url,  
                'oidc_token': {
                    'service_account_email': service_account
                }
            }
    }

    if payload is not None:
        converted_payload = payload.encode()

        task['http_request']['body'] = converted_payload

    if in_seconds is not None:
        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        task['schedule_time'] = timestamp

    try: response = client.create_task(parent, task)
    except:
        try:
            time.sleep(10)
            response = client.create_task(parent, task)
        except:
            create_queue(queue=queue, concurrent_dispatch=concurrent_dispatch)
            time.sleep(10)
            response = client.create_task(parent, task)

    print('Created task {}'.format(response.name))
    return response.name.split('/')[-1]

def create_queue(queue=queue, concurrent_dispatch=10):

    client = tasks_v2beta3.CloudTasksClient()

    parent = client.location_path(project, location)
    q = {
        'name': client.queue_path(project, location, queue),
        'app_engine_http_queue': {
            'app_engine_routing_override': {
                'service': 'default',
            },
        },
        'rate_limits': {
            'max_concurrent_dispatches': concurrent_dispatch,
        },
        'retry_config': {
            'max_attempts': 1,
        }
    }
    response = client.create_queue(parent, q)

    return response

