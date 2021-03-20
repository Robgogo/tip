from os import name
from django.contrib import admin
from django.urls import path, include, re_path
from rest_auth.views import LogoutView
from rest_auth.registration.views import VerifyEmailView, RegisterView

from api.views.kpis import AvailabiltyPerServiceViewSet, NumberOFIncidentsRaisedViewSet, SLAPerSeverityViewSet
from api.views.incidents import DepartmentViewSet, RaisedIncidentViewSet, ClosedIncidentViewSet, BacklogIncidentViewSet, CriticalIncidentViewSet, CriticalServiceViewSet, \
    DepartmentDetailViewSet, RaisedIncidentDetailViewSet, ClosedIncidentDetailViewSet, BacklogIncidentDetailViewSet, CriticalIncidentDetailViewSet, CriticalServiceDetailViewSet
from api.views.file_handler import DepartmentTableViewSet, IncidentTablesViewSet, CriticalIncidentTableViewSet, ServiceTableViewSet
from api.views.user import UserViewSet, GetLoggedInUserViewSet

urlpatterns = [
    # Admin paths
    path('admin/', include('rest_auth.urls')),
    path('admin/registration/', include('rest_auth.registration.urls')),
    re_path(r'^admin/logout/(?P<pk>[0-9a-f-]+)/$', LogoutView.as_view(), name='logout'),
    re_path(r'^admin/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^admin/account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('admin/user/myinfo/', GetLoggedInUserViewSet.as_view(), name='current-user'),
    re_path(r'^admin/users/(?P<pk>[0-9a-f-]+)/$', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='user-detail'),

    path('admin/raised_incident/', RaisedIncidentViewSet.as_view(), name='raised'),
    path('admin/closed_incident/', ClosedIncidentViewSet.as_view(), name='closed'),
    path('admin/backlog_incident/', BacklogIncidentViewSet.as_view(), name='backlog'),
    path('admin/critical_incident/', CriticalIncidentViewSet.as_view(), name='critical'),
    path('admin/department/', DepartmentViewSet.as_view(), name='department'),
    path('admin/critical-service/', CriticalServiceViewSet.as_view(), name='critical-service'),
    re_path(r'admin/raised_incident/(?P<id>[0-9a-f-]+)/$', RaisedIncidentDetailViewSet.as_view(), name='raised-incident-detail'),
    re_path(r'admin/closed_incident/(?P<id>[0-9a-f-]+)/$', ClosedIncidentDetailViewSet.as_view(), name='closed-incident-detail'),
    re_path(r'admin/backlog_incident/(?P<id>[0-9a-f-]+)/$', BacklogIncidentDetailViewSet.as_view(), name='backlog-incident-detail'),
    re_path(r'admin/critical_incident/(?P<id>[0-9a-f-]+)/$', CriticalIncidentDetailViewSet.as_view(), name='crirtical-incident-detail'),
    re_path(r'admin/department/(?P<id>[0-9a-f-]+)/$', DepartmentDetailViewSet.as_view(), name='department-detail'),
    re_path(r'admin/critical-service/(?P<id>[0-9a-f-]+)/$', CriticalServiceDetailViewSet.as_view(), name='critical-service-detail'),


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
