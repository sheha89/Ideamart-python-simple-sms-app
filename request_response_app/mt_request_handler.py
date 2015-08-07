import requests
import json
import ConfigParser

import logging

LOG = logging.getLogger("alert.service.mt.request.handler")

config = ConfigParser.ConfigParser()
config.read('properties.ini')


class MtRequestHandler(object):
    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.url = config.get('receiverUrl', 'url')

    def send_mt_request(self, mt_request_data):
        mt_request_json = {"message": mt_request_data.mt_message,
                           "destinationAddresses": mt_request_data.destination_address,
                           "password": mt_request_data.password, "applicationId": mt_request_data.application_id,
                           "encoding": mt_request_data.encoding, "version": mt_request_data.version}
        mt_request = json.dumps(mt_request_json)
        LOG.debug("MT Request : %s " % mt_request)
        mt_response = requests.post(self.url, data=mt_request, headers=self.headers)
        LOG.debug("MT Response : %s " % mt_response.text)
        LOG.debug("MT Message sent!!!")


class MtRequest(object):
    def __init__(self, request_data):
        self.data = json.loads(request_data)
        self.destination_address = self.data['sourceAddress']
        self.mt_message = self.data['message']
        self.password = "password"
        self.application_id = self.data['applicationId']
        self.version = self.data['version']
        self.encoding = self.data['encoding']
        self.request_id = self.data['requestId']
