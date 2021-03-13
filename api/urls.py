from os import name
from django.contrib import admin
from django.urls import path, include, re_path

from rest_auth.registration.views import VerifyEmailView, RegisterView

from api.views.kpis import AvailabiltyPerServiceViewSet, NumberOFIncidentsRaisedViewSet, SLAPerSeverityViewSet
from api.views.incidents import DepartmentViewSet, RaisedIncidentViewSet, ClosedIncidentViewSet, BacklogIncidentViewSet, CriticalIncidentViewSet, CriticalServiceViewSet
from api.views.file_handler import DepartmentTableViewSet, IncidentTablesViewSet, CriticalIncidentTableViewSet, ServiceTableViewSet

urlpatterns = [
    # Admin paths
    path('admin/', include('rest_auth.urls')),
    path('admin/registration/', include('rest_auth.registration.urls')),
    re_path(r'^admin/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^admin/account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),

    path('admin/raised_incident/', RaisedIncidentViewSet.as_view(), name='raised'),
    path('admin/closed_incident/', ClosedIncidentViewSet.as_view(), name='closed'),
    path('admin/backlog_incident/', BacklogIncidentViewSet.as_view(), name='backlog'),
    path('admin/critical_incident/', CriticalIncidentViewSet.as_view(), name='critical'),


    # kpi Paths
    re_path(r'kpi/num_incident/(?P<year>\d+)/(?P<month>\d+)/$', NumberOFIncidentsRaisedViewSet.as_view(), name='num_incident_kpi'),
    re_path(r'kpi/availability/(?P<year>\d+)/(?P<month>\d+)/$', AvailabiltyPerServiceViewSet.as_view(), name='availability_kpi'),
    re_path(r'kpi/sla/(?P<year>\d+)/(?P<month>\d+)/$', SLAPerSeverityViewSet.as_view(), name='sla_kpi'),

    # Table paths
    path('insert/department/', DepartmentTableViewSet.as_view(), name='insert_department'),
    path('insert/service/', ServiceTableViewSet.as_view(), name='insert_service'),
    path('insert/incident/', IncidentTablesViewSet.as_view(), name='insert_incident'),
    path('insert/critical/', CriticalIncidentTableViewSet.as_view(), name='insert_critical'),
]
