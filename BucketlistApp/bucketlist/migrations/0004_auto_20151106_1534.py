# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0003_auto_20151106_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bucketlistitems',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
