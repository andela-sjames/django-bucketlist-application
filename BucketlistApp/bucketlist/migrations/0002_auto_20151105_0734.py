# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucketlist',
            name='private',
        ),
        migrations.RemoveField(
            model_name='bucketlistitems',
            name='created_by',
        ),
        migrations.AddField(
            model_name='bucketlist',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bucketlistitems',
            name='name',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
