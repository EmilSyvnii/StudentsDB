# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students.

def students_list(request):
    students = (
        {'id': 1,
         'first_name': u'Даніель',
         'last_name': u'Аггер',
         'ticket': 5,
         'image': 'img/Agger.jpg'},
        {'id': 2,
         'first_name': u'Садіо',
         'last_name': u'Мане',
         'ticket': 19,
         'image': 'img/Sadio.jpeg'},
        {'id': 3,
         'first_name': u'Фернандо',
         'last_name': u'Торрес',
         'ticket': 9,
         'image': 'img/Nando.jpg'},
        {'id': 4,
         'first_name': u'Джордан',
         'last_name': u'Хендерсон',
         'ticket': 14,
         'image': 'img/Hendo.jpg'}
    )
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)


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