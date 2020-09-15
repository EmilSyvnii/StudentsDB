# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import messages
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper

from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))


    from_email = forms.EmailField(
        label=u"Ваша електронна адреса")

    subject = forms.CharField(
        label=u"Тема листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст листа",
        max_length=2560,
        widget=forms.Textarea)


def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with the data from the request:
        form = ContactForm(request.POST)

        # validation checking
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                messages.success(request, "Під час відправки листа виникла помилка, повторіть спробу пізніше.")
            else:
                messages.error(request, "Повідомлення успішно надіслано.")
            return HttpResponseRedirect(reverse('contact_admin'))

    # render blank form in case not POST
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})



