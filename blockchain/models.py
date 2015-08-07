from django.db import models
import pytz
import pyethereum
import rlp
import json
import requests
import datetime

# Create your models here.

class ByteField(models.CharField):
    """
    A field for storing binary objects of fixed length.
    Stored as a hexadecimal string beginning with "0x".
    """

    def __init__(self, *args, **kwargs):
        self.byte_length = kwargs['bytes']
        kwargs['max_length'] = self.byte_length * 2 + 2
        del kwargs['bytes']
        super(ByteField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ByteField, self).deconstruct()
        kwargs['bytes'] = self.byte_length
        del kwargs['max_length']
        return name, path, args, kwargs    

        
class Block(models.Model):
    number = models.IntegerField(primary_key=True)
    blockhash = ByteField(bytes=32)
    prevhash = ByteField(bytes=32)
    nonce = ByteField(bytes=8)
    uncles_hash = ByteField(bytes=32)
    logs_bloom = ByteField(bytes=256)
    transactions_root = ByteField(bytes=32)
    state_root = ByteField(bytes=32)
    miner = ByteField(bytes=20)
    difficulty = models.BigIntegerField()
    total_difficulty = models.BigIntegerField()
    extra_data = ByteField(bytes=32)
    gas_limit = models.BigIntegerField()
    gas_used = models.BigIntegerField()
    timestamp = models.DateTimeField()
    size = models.IntegerField()
    uncles = models.ManyToManyField('Block')
    
    def __init__(self, *args, **kwargs):
        if 'block_dict' in kwargs:
            block_dict = kwargs["block_dict"]
            del kwargs["block_dict"]
        else:
            block_dict = None
        super(Block, self).__init__(*args, **kwargs)
        if block_dict:
            self.from_dict(block_dict)
            
    def __unicode__(self):
        return "Block " + str(self.number) + " (" + str(self.timestamp) + ")"
    
    def from_dict(self, block):
        self.number = int(block[u"number"], 16)
        self.gas_limit = int(block["gasLimit"], 16)
        self.gas_used = int(block["gasUsed"], 16)
        self.logs_bloom = block["logsBloom"]
        self.nonce = block["nonce"]
        self.transactions_root = block["transactionsRoot"]
        self.blockhash = block["hash"]
        self.uncles_hash = block["sha3Uncles"]
        self.prevhash = block["parentHash"]
        self.extra_data = block["extraData"]
        self.miner = block["miner"]
        self.state_root = block["stateRoot"]
        self.difficulty = int(block["difficulty"], 16)
        self.total_difficulty = int(block["totalDifficulty"], 16)
        self.timestamp = datetime.datetime.fromtimestamp(int(block["timestamp"], 16), tz=pytz.utc)
        self.size = int(block["size"], 16)
        

      
    