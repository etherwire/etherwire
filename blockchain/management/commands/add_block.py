from django.core.management.base import BaseCommand, CommandError
from blockchain.models import Block
from blockchain.rpc import RPC_Client

class Command(BaseCommand):
    help = 'Loads one or more blocks into the database.'

    def add_arguments(self, parser):
        parser.add_argument('from_block', type=int)
        parser.add_argument('to_block', type=int)

    def handle(self, *args, **options):
        blocks = []
        client = RPC_Client(url="http://54.174.34.15:8402")
        for block_id in range(options['from_block'], options['to_block']):
            block_dict = client.get_block(block_id)
            new_block = Block(block_dict=block_dict)
            blocks.append(new_block)
            self.stdout.write('Successfully got %s' % new_block)
        Block.objects.bulk_create(blocks)
        self.stdout.write("Successfully saved all blocks.")