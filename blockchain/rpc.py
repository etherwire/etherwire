import requests
import json
import datetime

class RPC_Client(object):

    def __init__(self, *args, **kwargs):
        self.url = kwargs['url']
        self.request_id = 1        
        self.headers = {'context-type': 'application/json'}
    
    def get_block(self, block_id, return_transaction_objects=False):
        request_words = ['latest', 'pending', 'earliest']
        method = 'eth_getBlockByNumber'
        if isinstance(block_id, basestring):
            if block_id not in request_words:
                method = 'eth_getBlockByHash'
        else:
            block_id = hex(block_id)
        return self.send_request(method, [block_id, return_transaction_objects])
    
    def send_request(self, method, params):
        payload = {
          "jsonrpc": "2.0",
          "method": method,
          "params": params,
          "id": 1
        }
        response = requests.post(self.url, 
                                 data=json.dumps(payload), 
                                 headers=self.headers)
        decoded_response = json.loads(response.text)
        result = decoded_response["result"]
        return result


    