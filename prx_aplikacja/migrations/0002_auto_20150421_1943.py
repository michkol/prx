# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prx_aplikacja', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bramkaproxy',
            name='ip_liczba',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
