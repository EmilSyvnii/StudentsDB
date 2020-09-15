# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20171019_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430')),
                ('notes', models.TextField(verbose_name='\u041d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('leader', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0421\u0442\u0430\u0440\u043e\u0441\u0442\u0430', to='students.Student')),
            ],
            options={
                'verbose_name': '\u0413\u0440\u0443\u043f\u0430',
                'verbose_name_plural': '\u0413\u0440\u0443\u043f\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442', 'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442\u0438'},
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default='', max_length=256, verbose_name='\u041f\u043e \u0431\u0430\u0442\u044c\u043a\u043e\u0432\u0456', blank=True),
            preserve_default=True,
        ),
    ]
