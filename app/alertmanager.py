import requests
import json
import logging
from requests.auth import HTTPBasicAuth

def alert(event,config,thisHost,timestamp):
  logger = logging.getLogger('main') 
  tags = "NA"
  actorName = "NA"
  actorImage = "NA"

  if 'tags' in config['settings']:
    tags = ", ".join([str(x) for x in config['settings']['tags']])

  if 'name' in event['Actor']['Attributes']:    
    actorName = event['Actor']['Attributes']['name']
  
  if 'image' in event['Actor']['Attributes']:
    actorImage = event['Actor']['Attributes']['image']

  payload = [{
	  "status": "firing",
	  "labels": {
	  	"alertname": f"DEM_{event['Type']}",
      "image": actorImage,
      "instance": thisHost,
      "job": "dem",
      "name": actorName,
      "type": event['Type'],
      "action": event['Action'],
      "severity": config['settings']['logging']
    },
    "annotations": {"tags": tags}
	}]

  alertmanager_config = config['integrations']['alertmanager']

  # Is basic_auth enabled?
  if 'basic_auth' in alertmanager_config:

    auth = alertmanager_config['basic_auth']

    ## Perform request
    try:
      requests.post(
        alertmanager_config['url'],
        data = json.dumps(payload),
        headers = {'Content-Type': 'application/json'},
        auth=HTTPBasicAuth(auth['username'], auth['password'])
      )

    except requests.exceptions.RequestException as e:
      logger.error('{}: {}'.format(__name__,e))

  else:
    ## Perform request
    try:
      requests.post(
        alertmanager_config['url'],
        data = json.dumps(payload),
        headers = {'Content-Type': 'application/json'}
      )

    except requests.exceptions.RequestException as e:
      logger.error('{}: {}'.format(__name__,e))
