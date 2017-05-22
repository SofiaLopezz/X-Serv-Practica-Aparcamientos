# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 11:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0003_auto_20170521_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estilo',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='guardado',
            name='aparcamiento',
        ),
        migrations.RemoveField(
            model_name='guardado',
            name='usuario',
        ),
        migrations.AddField(
            model_name='usuario',
            name='color',
            field=models.CharField(default='black', max_length=20),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 21, 11, 28, 55, 3077)),
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre_pagina',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='size',
            field=models.IntegerField(default='1'),
        ),
        migrations.DeleteModel(
            name='Estilo',
        ),
        migrations.DeleteModel(
            name='Guardado',
        ),
    ]