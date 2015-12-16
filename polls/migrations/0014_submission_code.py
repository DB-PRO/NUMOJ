# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_problem_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='code',
            field=models.CharField(default='..code..', max_length=1000),
        ),
    ]
