# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from datetime import datetime, date
from django.core.urlresolvers import reverse
from calendar import monthrange, weekday, day_abbr
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse

from django.views.generic import TemplateView

from ..models import Student, Group, MonthJournal
from ..util import paginate


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)

        # checking if the data was sent via params
        # if not just set the current date
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['cur_month'] = month.strftime('%Y-%m-%d')
        context['month_verbose'] = month.strftime('%B')

        # prepare vars for template to generate journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{
            'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days+1)]

        if kwargs.get('pk'):
            queryset = Student.objects.filter(pk=kwargs['pk'])
        else:
            queryset = Student.objects.order_by('last_name')
        
        # set url for AJAX request
        update_url = reverse('journal')

        students = []
        for student in queryset:
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })
            # preparing metadata for current student
            students.append({
                'fullname': '%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        context = paginate(students, 10, self.request, context, var_name='students')

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        current_date = datetime.strptime((data['date']), '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])            # get student's object from the database with ID

        # get or create journal obj
        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

        # set new presence in journal for given stud and save the results
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        # return success status
        return JsonResponse({'status': 'success'})