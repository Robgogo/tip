from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from api.models.incidents import Department, CriticalService, \
    ClosedIncident, RaisedIncident, CriticalIncident, BacklogIncident
from api.serializers.incidents import DepartmentSerializer, CriticalServiceSerializer, \
    RaisedIncidentSerializer, ClosedIncidentSerializer, BacklogIncidentSerializer, CriticalIncidentSerializer


class DepartmentViewSet(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == 1:
                serialzed = DepartmentSerializer(self.queryset, context={'request': request}, many=True)
                return Response(data=serialzed.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CriticalServiceViewSet(ListCreateAPIView):
    queryset = CriticalService.objects.all()
    serializer_class = CriticalServiceSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == 1:
                serialzed = CriticalServiceSerializer(self.queryset, context={'request': request}, many=True)
                return Response(data=serialzed.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class IncidentViewSet(ListCreateAPIView):
#     queryset = Incident.objects.all()
#     serializer_class = IncidentSerializer
#     permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

#     def get(self, request, *args, **kwargs):
#         try:
#             if request.user.role == 1:
#                 serialzed = IncidentSerializer(self.queryset, context={'request': request}, many=True)
#                 return Response(data=serialzed.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RaisedIncidentViewSet(ListCreateAPIView):
    queryset = RaisedIncident.objects.all()
    serializer_class = RaisedIncidentSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == 1:
                serialzed = RaisedIncidentSerializer(self.queryset, context={'request': request}, many=True)
                return Response(data=serialzed.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClosedIncidentViewSet(ListCreateAPIView):
    queryset = ClosedIncident.objects.all()
    serializer_class = ClosedIncidentSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == 1:
                serialzed = ClosedIncidentSerializer(self.queryset, context={'request': request}, many=True)
                return Response(data=serialzed.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BacklogIncidentViewSet(ListCreateAPIView):
    queryset = BacklogIncident.objects.all()
    serializer_class = BacklogIncidentSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == 1:
                serialzed = BacklogIncidentSerializer(self.queryset, context={'request': request}, many=True)
                return Response(data=serialzed.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CriticalIncidentViewSet(ListCreateAPIView):
    queryset = CriticalIncident.objects.all()
    serializer_class = CriticalIncidentSerializer
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            if request.user.role == 1:
                serialzed = CriticalIncidentSerializer(self.queryset, context={'request': request}, many=True)
                return Response(data=serialzed.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
