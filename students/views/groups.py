# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.forms import ModelForm

from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions

from ..models import Group

# Views for Groups

class GroupListView(ListView):
    queryset = Group.objects.all()
    template_name = 'groups/groups_list_CBV.html'
    context_object_name = 'groups_list'
    paginate_by = 3

    # ordering
    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('title',):
            ordered_groups = Group.objects.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                ordered_groups = ordered_groups.reverse()
            return ordered_groups
        else:
            return Group.objects.order_by('title')




class GroupAddForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('groups_add')

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', 'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', 'Скасувати', css_class="btn btn-link"),
        )


class GroupAddView(CreateView):
    model = Group
    template_name = 'groups/groups_add.html'
    form_class = GroupAddForm

    def get_success_url(self):
        messages.success(self.request, "Групу успішно додано")
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, "Зміни скасовано")
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)


class GroupEditForm(GroupAddForm):

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)

        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})


class GroupEditView(UpdateView):
    model = Group
    template_name = 'groups/groups_edit.html'
    form_class = GroupEditForm

    def get_success_url(self):
        messages.success(self.request, "Зміни збережено")
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, "Зміни скасовано")
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupEditView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'groups/groups_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Групу успішно видалено")
        return reverse('groups')
