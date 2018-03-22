
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
#from django.conf.urls.static import static
#from django.conf import settings
from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.groups import GroupListView, GroupAddView, GroupEditView, GroupDeleteView

urlpatterns = patterns('',

    # Students urls

    url(r'^$', 'students.views.students.students_list', name='home'),

    url(r'^students/add/$', 'students.views.students.students_add', name='students_add'),

    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),

    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    url(r'^journal/$', 'students.views.journal.journal_list', name='journal'),

    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),

    # Groups urls

    url(r'^groups/$', GroupListView.as_view(), name='groups'),

    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),

    url(r'^groups/(?P<pk>\d+)/edit/$', GroupEditView.as_view(), name='groups_edit'),

    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),

    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : MEDIA_ROOT}))

    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
