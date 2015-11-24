# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0002_auto_20151119_1540'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BucketlistItems',
            new_name='BucketlistItem',
        ),
    ]
