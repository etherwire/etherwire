# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import blockchain.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('blockhash', blockchain.models.ByteField(bytes=32)),
                ('prevhash', blockchain.models.ByteField(bytes=32)),
                ('nonce', blockchain.models.ByteField(bytes=8)),
                ('uncles_hash', blockchain.models.ByteField(bytes=32)),
                ('logs_bloom', blockchain.models.ByteField(bytes=256)),
                ('transactions_root', blockchain.models.ByteField(bytes=32)),
                ('state_root', blockchain.models.ByteField(bytes=32)),
                ('miner', blockchain.models.ByteField(bytes=20)),
                ('difficulty', models.BigIntegerField()),
                ('total_difficulty', models.BigIntegerField()),
                ('extra_data', blockchain.models.ByteField(bytes=32)),
                ('gas_limit', models.BigIntegerField()),
                ('gas_used', models.BigIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('size', models.IntegerField()),
                ('uncles', models.ManyToManyField(to='blockchain.Block')),
            ],
        ),
    ]
