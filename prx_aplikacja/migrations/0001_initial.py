# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BramkaProxy',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('adres', models.URLField(max_length=255)),
                ('adres_k', models.CharField(max_length=255)),
                ('kraj', models.CharField(max_length=2)),
                ('ip', models.GenericIPAddressField(protocol='IPv4')),
                ('ip_indeks', models.PositiveIntegerField(null=True)),
                ('ip_liczba', models.PositiveIntegerField()),
                ('ping', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('ost_spr_ip', models.DateTimeField()),
                ('ost_spr_ping', models.DateTimeField()),
                ('ip_blad', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'bramki_proxy',
            },
        ),
    ]
