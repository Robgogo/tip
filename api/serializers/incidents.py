from rest_framework import serializers

from api.models.incidents import Department, CriticalService, \
    ClosedIncident, RaisedIncident, CriticalIncident, BacklogIncident


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='department-detail')

    class Meta:
        model = Department
        fields = ['url', 'department_code', 'department_name', 'department_desc']


class CriticalServiceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='critical-service-detail')

    class Meta:
        model = CriticalService
        fields = ['url', 'id', 'service', 'application']


# class IncidentSerializer(serializers.HyperlinkedModelSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name='incident-detail')
#     department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

#     class Meta:
#         model = Incident
#         fields = ['url', 'incident_id', 'priority', 'incident_type', 'department', 'incident_status']


class RaisedIncidentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='incident-raised-detail')
    department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

    class Meta:
        model = RaisedIncident
        fields = ['url', 'incident_id', 'priority', 'incident_type', 'department', 'incident_status', 'created_date', 'resolution_date']


class ClosedIncidentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='incident-raised-detail')
    department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

    class Meta:
        model = ClosedIncident
        fields = ['url', 'incident_id', 'priority', 'incident_type', 'department', 'incident_status', 'created_date', 'resolution_date']


class CriticalIncidentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='incident-raised-detail')
    # incident_id = serializers.HyperlinkedRelatedField(view_name='incident-detail', read_only=True)
    application = serializers.HyperlinkedRelatedField(view_name='critical-service-detail', read_only=True)

    class Meta:
        model = CriticalIncident
        fields = ['url', 'incident_id', 'created_date', 'resolution_date', 'application', 'priority', 'incident_status']


class BacklogIncidentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='incident-raised-detail')
    department = serializers.HyperlinkedRelatedField(view_name='department-detail', read_only=True)

    class Meta:
        model = BacklogIncident
        fields = ['url', 'incident_id', 'priority', 'incident_type', 'department', 'incident_status', 'created_date', 'resolution_date']
