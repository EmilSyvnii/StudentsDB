# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Views for Groups

def groups_list(request):
    groups = (
        {'id': 1,
         'group_name': 'ЛФК-1',
         'group_leader': u'Хендерсон Джордан'},
        {'id': 2,
         'group_name': 'ЛФК-2',
         'group_leader': u'Аггер Даніель'},
        {'id': 3,
         'group_name': 'ЛФК-3',
         'group_leader': u'Торрес Фернандо'}
    )
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)