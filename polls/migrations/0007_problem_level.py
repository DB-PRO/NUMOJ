# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_remove_submission_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
