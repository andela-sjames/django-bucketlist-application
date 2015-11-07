# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0005_auto_20151107_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bucketlist',
            options={'ordering': ('date_created',)},
        ),
        migrations.AlterModelOptions(
            name='bucketlistitems',
            options={'ordering': ('date_created',)},
        ),
    ]
