from rest_framework import serializers

from api.models.incidents import Department, CriticalService, \
    ClosedIncident, RaisedIncident, CriticalIncident, BacklogIncident


class DepartmentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='department-detail')

    class Meta:
        model = Department
        fields = ['department_code', 'department_name', 'department_desc']


class CriticalServiceSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='critical-service-detail')

    class Meta:
        model = CriticalService
        fields = ['id', 'service', 'application']


# class IncidentSerializer(serializers.HyperlinkedModelSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name='incident-detail')
#     department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

#     class Meta:
#         model = Incident
#         fields = ['url', 'incident_id', 'priority', 'incident_type', 'department', 'incident_status']


class RaisedIncidentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='raised-incident-detail')
    # department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

    class Meta:
        model = RaisedIncident
        fields = ['incident_id', 'priority', 'incident_type', 'department', 'incident_status', 'created_date', 'resolution_date']


class ClosedIncidentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='closed-incident-detail')
    # department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

    class Meta:
        model = ClosedIncident
        fields = ['incident_id', 'priority', 'incident_type', 'department', 'incident_status', 'created_date', 'resolution_date']


class CriticalIncidentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='critical-incident-detail')
    # # incident_id = serializers.HyperlinkedRelatedField(view_name='incident-detail', read_only=True)
    # application = serializers.HyperlinkedRelatedField(view_name='critical-service-detail', read_only=True)

    class Meta:
        model = CriticalIncident
        fields = ['incident_id', 'created_date', 'resolution_date', 'application', 'priority', 'incident_status']


class BacklogIncidentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='backlog-incident-detail')
    # department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

    class Meta:
        model = BacklogIncident
        fields = ['incident_id', 'priority', 'incident_type', 'department', 'incident_status', 'created_date', 'resolution_date']
