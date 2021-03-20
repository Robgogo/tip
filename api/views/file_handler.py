import os
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import FileUploadParser

from api.helpers.process_excel import application_service_excel_handler, department_excel_handler, critical_incidents_excel_handler,\
    backlog_incidents_excel_handler, raised_incidents_excel_handler, closed_incidents_excel_handler
from api.serializers.file_upload import UploadSerializer


class DepartmentTableViewSet(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadSerializer
    # parser_classes = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # if request.user.role != 1:
        #     return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            file_uploaded = request.FILES.get('file')
            with open(file_uploaded.name, 'wb+') as f:
                for chunk in file_uploaded.chunks():
                    f.write(chunk)
            
            response = department_excel_handler(file_uploaded.name)
            if response == 'Success':
                os.remove(file_uploaded.name)
                return Response(data={"message": "File uploaded and loaded succesfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Loading data failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceTableViewSet(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadSerializer
    # parser_classes = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # if request.user.role != 1:
        #     return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            file_uploaded = request.FILES.get('file')
            with open(file_uploaded.name, 'wb+') as f:
                for chunk in file_uploaded.chunks():
                    f.write(chunk)
            
            response = application_service_excel_handler(file_uploaded.name)
            if response == 'Success':
                os.remove(file_uploaded.name)
                return Response(data={"message": "File uploaded and loaded succesfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Loading data failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response(data={'message': "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CriticalIncidentTableViewSet(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadSerializer
    # parser_classes = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # if request.user.role != 1:
        #     return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            file_uploaded = request.FILES.get('file')
            with open(file_uploaded.name, 'wb+') as f:
                for chunk in file_uploaded.chunks():
                    f.write(chunk)
            
            response = critical_incidents_excel_handler(file_uploaded.name)
            if response == 'Success':
                os.remove(file_uploaded.name)
                return Response(data={"message": "File uploaded and loaded succesfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Loading data failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(data={'message': f"Something went wrong! {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncidentTablesViewSet(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadSerializer
    # parser_classes = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # if request.user.role != 1:
        #     return Response(data={'message': "You need Admin ROLE to access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            print(request.FILES)
            file_uploaded = request.FILES.get('file')
            print(file_uploaded)
            with open(file_uploaded.name, 'wb+') as f:
                for chunk in file_uploaded.chunks():
                    f.write(chunk)
            
            response_raised = raised_incidents_excel_handler(file_uploaded.name)
            response_backlog = backlog_incidents_excel_handler(file_uploaded.name)
            response_closed = closed_incidents_excel_handler(file_uploaded.name)
            if response_closed == 'Success' and response_backlog == 'Success' and response_raised == 'Success':
                os.remove(file_uploaded.name)
                return Response(data={"message": "File uploaded and loaded succesfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Loading data failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response(data={'message': f"Something went wrong! {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
