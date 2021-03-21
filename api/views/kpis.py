# TODO: Implement KPI related views
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from api.models.incidents import Department, CriticalService, \
    ClosedIncident, RaisedIncident, CriticalIncident, BacklogIncident
from api.serializers.incidents import DepartmentSerializer, CriticalServiceSerializer, \
    RaisedIncidentSerializer, ClosedIncidentSerializer, BacklogIncidentSerializer, CriticalIncidentSerializer
from api.serializers.user import UserSerializer


class NumberOFIncidentsRaisedViewSet(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        if request.user.role == 3:
            return Response(data={'message': "You need Admin or Manager ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            year = kwargs['year']
            month = kwargs['month']
            raised_incidents = RaisedIncident.objects.all()
            backlog_incidents = BacklogIncident.objects.all()
            # Previous month data
            low_severity_pre = RaisedIncidentSerializer([], context={"request": request}, many=True)
            medium_severity_pre = RaisedIncidentSerializer([], context={"request": request}, many=True)
            high_severity_pre = RaisedIncidentSerializer([], context={"request": request}, many=True)
            critical_severity_pre = RaisedIncidentSerializer([], context={"request": request}, many=True)
            backlog_pre = BacklogIncidentSerializer([], context={"request": request}, many=True)
            if int(month) > 1:
                low_severity_pre = RaisedIncidentSerializer(raised_incidents.filter(priority="Baja", created_date__year=year, created_date__month=int(month) - 1), context={"request": request}, many=True)
                medium_severity_pre = RaisedIncidentSerializer(raised_incidents.filter(priority="Media", created_date__year=year, created_date__month=int(month) - 1), context={"request": request}, many=True)
                high_severity_pre = RaisedIncidentSerializer(raised_incidents.filter(priority="Alta", created_date__year=year, created_date__month=int(month) - 1), context={"request": request}, many=True)
                critical_severity_pre = RaisedIncidentSerializer(raised_incidents.filter(priority="Crítica", created_date__year=year, created_date__month=int(month) - 1), context={"request": request}, many=True)
                backlog_pre = BacklogIncidentSerializer(backlog_incidents.filter(for_month=int(month) - 1), context={"request": request}, many=True)

            backlog = BacklogIncidentSerializer(backlog_incidents.filter(for_month=int(month)), context={"request": request}, many=True)
            low_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Baja", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            medium_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Media", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            high_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Alta", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            critical_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Crítica", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            low_sev_diff = (len(low_severity.data) - len(low_severity_pre.data)) / len(low_severity_pre.data) if (low_severity_pre and len(low_severity_pre.data) > 0) else 1
            low_sev_diff = low_sev_diff * 100
            medium_sev_diff = (len(medium_severity.data) - len(medium_severity_pre.data)) / len(medium_severity_pre.data) if (medium_severity_pre and len(medium_severity_pre.data) > 0) else 1
            medium_sev_diff = medium_sev_diff * 100
            high_sev_diff = (len(high_severity.data) - len(high_severity_pre.data)) / len(high_severity_pre.data) if (high_severity_pre and len(high_severity_pre.data) > 0) else 1
            high_sev_diff = high_sev_diff * 100
            critical_sev_diff = (len(critical_severity.data) - len(critical_severity_pre.data)) / len(critical_severity_pre.data) if (critical_severity_pre and len(critical_severity_pre.data) > 0) else 1
            critical_sev_diff = critical_sev_diff * 100
            backlog_diff = (len(backlog.data) - len(backlog_pre.data)) / len(backlog_pre.data) if (backlog and len(backlog_pre.data) > 0) else 1
            backlog_diff = backlog_diff * 100

            resp = {
                "critical": {"incident": len(critical_severity.data), "difference": critical_sev_diff},
                "backlog": {"incident": len(backlog.data), "difference": backlog_diff},
                "medium": {"incident": len(medium_severity.data), "difference": medium_sev_diff},
                "high": {"incident": len(high_severity.data), "difference": high_sev_diff},
                "low": {"incident": len(low_severity.data), "difference": low_sev_diff},
                "incidents": RaisedIncidentSerializer(raised_incidents, context={"request": request}, many=True).data,
                "user": UserSerializer(request.user, context={'request': request}).data
            }
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AvailabiltyPerServiceViewSet(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        if request.user.role == 3:
            return Response(data={'message': "You need Admin or Manager ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            availability = {}
            year = kwargs['year']
            month = kwargs['month']
            services = CriticalService.objects.all()
            for service in services:
                availability[service.service] = {"total_unavailable_time": 0, "availability": 0}
            
            critical_incidents = CriticalIncident.objects.filter(created_date__year=year, created_date__month=month)
            # print(critical_incidents)
            for incident in critical_incidents:
                if incident.application:
                    service = incident.application.service
                    time_delta = incident.resolution_date - incident.created_date
                    availability[service]['total_unavailable_time'] += time_delta.total_seconds()
            for serv in availability:
                availability[serv]["availability"] = (1 - (availability[serv]["total_unavailable_time"] / (30 * 24 * 3600))) * 100
            return Response(data=availability, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': f"Something went wrong! {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SLAPerSeverityViewSet(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        if request.user.role == 3:
            return Response(data={'message': "You need Admin or Manager ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sla = {
                "low": {
                    "in_sla": 0,
                    "out_sla": 0
                },
                "medium": {
                    "in_sla": 0,
                    "out_sla": 0
                },
                "high": {
                    "in_sla": 0,
                    "out_sla": 0
                },
                "critical": {
                    "in_sla": 0,
                    "out_sla": 0
                }
            }
            year = kwargs['year']
            month = kwargs['month']
            closed_incidents = ClosedIncident.objects.all()
            low_severity = closed_incidents.filter(priority="Baja", resolution_date__year=year, resolution_date__month=month)
            medium_severity = closed_incidents.filter(priority="Media", resolution_date__year=year, resolution_date__month=month)
            high_severity = closed_incidents.filter(priority="Alta", resolution_date__year=year, resolution_date__month=month)
            critical_severity = closed_incidents.filter(priority="Crítica", resolution_date__year=year, resolution_date__month=month)
            for low in low_severity:
                time_delta = low.resolution_date - low.created_date
                sla_time = 15 * 24
                time_to_resolve = time_delta.total_seconds() / 3600
                if time_to_resolve <= sla_time:
                    sla['low']['in_sla'] += 1
                else:
                    sla['low']['out_sla'] += 1
            
            for medium in medium_severity:
                time_delta = medium.resolution_date - medium.created_date
                sla_time = 5 * 24
                time_to_resolve = time_delta.total_seconds() / 3600
                if time_to_resolve <= sla_time:
                    sla['medium']['in_sla'] += 1
                else:
                    sla['medium']['out_sla'] += 1

            for high in high_severity:
                time_delta = high.resolution_date - high.created_date
                sla_time = 8
                time_to_resolve = time_delta.total_seconds() / 3600
                if time_to_resolve <= sla_time:
                    sla['high']['in_sla'] += 1
                else:
                    sla['high']['out_sla'] += 1

            for critical in critical_severity:
                time_delta = critical.resolution_date - critical.created_date
                sla_time = 4
                time_to_resolve = time_delta.total_seconds() / 3600
                if time_to_resolve <= sla_time:
                    sla['critical']['in_sla'] += 1
                else:
                    sla['critical']['out_sla'] += 1

            return Response(data=sla, status=status.HTTP_200_OK)         
        except Exception as e:

            return Response(data={'message': f"Something went wrong!{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
