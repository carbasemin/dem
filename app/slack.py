import requests
import time
import json
import logging

def alert(event,config,thisHost,timestamp):
  logger = logging.getLogger('main') 
  tags = "NA"
  actorName = "NA"

  if 'tags' in config['settings']:
    tags = ", ".join([str(x) for x in config['settings']['tags']])

  if 'name' in event['Actor']['Attributes']:    
    actorName = event['Actor']['Attributes']['name']

  payloadText = "*Host*: {}, *Type*: {}, *Action*: {}, *Name*: {}, *Tags*: {}".format(thisHost, event['Type'], event['Action'], actorName, tags)
  muteAlert = False
  if event['Type'] == "service" and event['Action'] == "update":
    if "updatestate.new" in event['Actor']['Attributes']:
      payloadText = "*Host*: {}, *Type*: {}, *Action*: {}, *Name*: {}, *Update State*: {} *Tags*: {}".format(
        thisHost, event['Type'],
        event['Action'],
        actorName,
        event['Actor']['Attributes']['updatestate.new'],
        tags)
    else:
      ## Mute update only alerts (happens when a stack deploy runs but does not actually change anything)
      muteAlert = True

  ## Compact Payload
  payload = {
    "username" : "DEM",
      "text": payloadText,
      "blocks": [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": payloadText
          }
        }
      ]
  }

  ## Perform request
  try:
    if not muteAlert:
      requests.post(
        config['integrations']['slack']['url'], 
        data = json.dumps(payload),
        headers = {'Content-Type': 'application/json'}
      )

  except requests.exceptions.RequestException as e:
    logger.error('{}: {}'.format(__name__,e))