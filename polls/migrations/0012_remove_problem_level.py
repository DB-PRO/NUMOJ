# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20151204_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='level',
        ),
    ]
