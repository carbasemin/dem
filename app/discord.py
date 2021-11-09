import requests
import time
import json
import logging

def alert(event,config,thisHost,timestamp):
  logger = logging.getLogger('main')

  ## Define payload
  payload = {
    "embeds": [{
      "fields": [
        {
          "name": "Host",
          "value": thisHost,
          "inline": True
        },
        {
          "name": "Type",
          "value": event['Type'],
          "inline": True
        },
        {
          "name": "Time",
          "value": timestamp,
          "inline": True
        },
        {
          "name": "Action",
          "value": event['Action'],
          "inline": True
        },
        {
          "name": "ID",
          "value": event['Actor']['ID']
        }
      ]
    }]
  }

  ## Append name to payload if exists
  if 'name' in event['Actor']['Attributes']:
    nameField = {
      "name": "Name",
      "value": event['Actor']['Attributes']['name']
    }
    payload['embeds'][0]['fields'].append(nameField)

  ## Append tags to payload if exists
  if 'tags' in config['settings']:
    tags = ", ".join([str(x) for x in config['settings']['tags']])
    tagsField = {
      "name": "Tags",
      "value": tags,
    }
    payload['embeds'][0]['fields'].append(tagsField)    
  
  ## Perform request
  try:
    requests.post(
      config['integrations']['discord']['url'], 
      data = json.dumps(payload),
      headers = {'Content-Type': 'application/json'}
    )

  except requests.exceptions.RequestException as e:
    logger.error('{}: {}'.format(__name__,e))
    
