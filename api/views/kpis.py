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


class NumberOFIncidentsRaisedViewSet(ListAPIView):
    # permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # if request.user.role == 3:
        #     return Response(data={'message': "You need Admin or Manager ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            year = kwargs['year']
            month = kwargs['month']
            raised_incidents = RaisedIncident.objects.all()
            backlog_incidents = BacklogIncidentSerializer(BacklogIncident.objects.all(), context={"request": request}, many=True)
            low_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Baja", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            medium_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Media", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            high_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Alta", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            critical_severity = RaisedIncidentSerializer(raised_incidents.filter(priority="Crítica", created_date__year=year, created_date__month=month), context={"request": request}, many=True)
            resp = {
                "critical": len(critical_severity.data),
                "backlog": len(backlog_incidents.data),
                "medium": len(medium_severity.data),
                "high": len(high_severity.data),
                "low": len(low_severity.data),
                "incidents": RaisedIncidentSerializer(raised_incidents, context={"request": request}, many=True).data
            }
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AvailabiltyPerServiceViewSet(ListAPIView):
    # permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # if request.user.role == 3:
        #     return Response(data={'message': "You need Admin or Manager ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            availability = {}
            year = kwargs['year']
            month = kwargs['month']
            services = CriticalService.objects.all()
            for service in services:
                availability[service.service] = {"total_unavailable_time": 0, "availability": 0}
            
            critical_incidents = CriticalIncident.objects.filter(created_date__year=year, created_date__month=month)
            for incident in critical_incidents:
                service = incident.application.service
                time_delta = incident.resolution_date - incident.created_date
                availability[service]['total_unavailable_time'] += time_delta.total_seconds()
            for serv in availability:
                availability[serv]["availability"] = (1 - (availability[serv]["total_unavailable_time"] / (30 * 24 * 3600))) * 100
            return Response(data=availability, status=status.HTTP_200_OK)
        except Exception as e:
            Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SLAPerSeverityViewSet(ListAPIView):
    # permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # if request.user.role == 3:
        #     return Response(data={'message': "You need Admin or Manager ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
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
            low_severity = closed_incidents.filter(priority="Baja", created_date__year=year, created_date__month=month)
            medium_severity = closed_incidents.filter(priority="Media", created_date__year=year, created_date__month=month)
            high_severity = closed_incidents.filter(priority="Alta", created_date__year=year, created_date__month=month)
            critical_severity = closed_incidents.filter(priority="Crítica", created_date__year=year, created_date__month=month)
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
