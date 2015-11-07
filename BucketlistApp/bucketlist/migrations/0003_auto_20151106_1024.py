# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0002_auto_20151105_0734'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bucketlist',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='bucketlistitems',
            options={'ordering': ('name',)},
        ),
    ]
