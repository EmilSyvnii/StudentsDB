# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm

from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions

from ..models import Student, Group
from ..util import paginate

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
                messages.success(request, ("Студента %s %s успішно додано" % (data['first_name'], data['last_name'])))
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                messages.warning(request, "Поля заповнено некоректно")
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            messages.success(request, "Додавання студента скасовано")
            return HttpResponseRedirect(reverse('home'))

    else:
        return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title')})

    return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', 'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', 'Скасувати', css_class="btn btn-link"),
        )


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        messages.success(self.request, "Зміни збережено")
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, "Зміни скасовано")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Студента успішно видалено")
        return reverse('home')
