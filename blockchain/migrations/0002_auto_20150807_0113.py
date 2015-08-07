# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='id',
        ),
        migrations.AlterField(
            model_name='block',
            name='number',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
