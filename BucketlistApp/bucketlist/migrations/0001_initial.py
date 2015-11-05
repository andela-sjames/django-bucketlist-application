# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import bucketlist.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucketlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('private', models.BooleanField(default=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_modified', bucketlist.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=100, blank=True)),
                ('user', models.ForeignKey(related_query_name=b'buckets', related_name='bucket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BucketlistItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_modified', bucketlist.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('done', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=100, blank=True)),
                ('bucketlist', models.ForeignKey(related_query_name=b'items', related_name='item', to='bucketlist.Bucketlist')),
            ],
        ),
    ]
