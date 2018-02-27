# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from datetime import datetime

from ..models import Student, Group

# Views for Students.

def students_list(request):
    students = Student.objects.all()

    #ordering
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket', 'student_group'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')

    #pagination
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:

            errors = {}

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть у форматі Рік-місяць-день"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білету є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть існуючу групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            if not errors:
                student = Student(**data)
                student.save()
                # redirection to students list
                return HttpResponseRedirect(u'%s?status_message=Студента %s %s успішно додано.' %
                                            (reverse('home'), data['first_name'], data['last_name']))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано' % reverse('home'))

    else:
        return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title')})

    return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)
