# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0004_auto_20151106_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='user',
            field=models.ForeignKey(related_name='buckets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bucketlistitems',
            name='bucketlist',
            field=models.ForeignKey(related_name='items', to='bucketlist.Bucketlist'),
        ),
    ]
