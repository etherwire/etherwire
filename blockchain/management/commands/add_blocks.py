from django.core.management.base import BaseCommand, CommandError
from blockchain.models import Block
from blockchain.rpc import RPC_Client
from django.conf import settings
import time

class Command(BaseCommand):
    help = 'Loads one or more blocks into the database.'

    def getBlocks(self, min, max):
        blocks = []
        for block_number in range(min, max):
            block_dict = self.client.get_block(block_number)
            new_block = Block(block_dict=block_dict)
            blocks.append(new_block)
            self.stdout.write('Successfully got %s' % new_block)
        Block.objects.bulk_create(blocks)

    def updateBlocks(self):
        # get latest block in database
        (db_num, db_hash, db_parent) = Block.objects.order_by('-number').values_list('number', 'blockhash', 'prevhash')[0]            
        # check that all blocks are included
        if db_num != Block.objects.count() - 1:
            raise Exception("Missing at least one block.")
        
        # compare it to the same block from RPC to make sure that hasn't changed
        compare_block = self.client.get_block(db_num)
        if compare_block["hash"] != db_hash:
            (revising_num, revising_parent) = (db_num, db_parent)
            print "Revising block %d (%s)" % (revising_num, revising_parent)
            new_block = Block(block_dict=compare_block)
            new_block.save()
        print compare_block["hash"]
        print db_hash
        print int(compare_block["number"], 16)
        print db_num
        if compare_block["hash"] != db_hash:
            (revising_num, revising_parent) = (db_num, db_parent)
            self.stdout.write("Revising block %d (%s)" % (revising_num, revising_parent))
            new_block = Block(block_dict=compare_block)
            new_block.save()
            # check previous blocks
            while revising_parent != compare_block["parentHash"]:
                revising_num = revising_num - 1
                self.stdout.write("Revising block %d (%s)" % (db_num, db_parent))
                revising_parent = Block.objects.get(number=db_num).prevhash
                new_block = Block(block_dict=client.get_block(db_num))
                new_block.save()
                compare_block = self.client.get_block(revising_num)
                db_parent = Block.objects.get(number=db_num).prevhash
                new_block = Block(block_dict=client.get_block(db_num))
                new_block.save()
        
        # find the latest block and update up to it
        latest_block_num = int(self.client.get_block("latest")["number"], 16)
        self.getBlocks(db_num + 1, latest_block_num)
        time.sleep(2)

    def handle(self, *args, **options):
        self.client = RPC_Client()

        if Block.objects.count() == 0:
            # get first two blocks so that logic works
            self.getBlocks(0, 2)

        while True:
            self.updateBlocks()


