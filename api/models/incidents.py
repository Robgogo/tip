import uuid
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import NullBooleanField


class Department(models.Model):
    department_code = models.CharField(max_length=50, primary_key=True)
    department_name = models.CharField(max_length=50)
    department_desc = models.CharField(max_length=50)

    def __repr__(self):
        return self.department_code
    
    def __str__(self):
        return self.department_code


# class Incident(models.Model):

#     STATUS = (
#         ('PENDING', 'PENDING'),
#         ('RESOLVED', 'RESOLVED'),
#         ('CLOSED', 'CLOSED'),
#         ('OPEN', 'OPEN'),
#     )

#     incident_id = models.CharField(max_length=50, primary_key=True)
#     priority = models.CharField(max_length=50)
#     incident_type = models.CharField(max_length=250)
#     department = models.ForeignKey(Department, on_delete=CASCADE)
#     incident_status = models.CharField(max_length=50, choices=STATUS)

#     def __repr__(self):
#         return self.incident_id
    
#     def __str__(self):
#         return self.incident_id


class CriticalService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(max_length=50)
    application = models.CharField(max_length=50)

    def __repr__(self):
        return self.application
    
    def __str__(self):
        return self.application


class RaisedIncident(models.Model):

    STATUS = (
        ('PENDING', 'PENDING'),
        ('RESOLVED', 'RESOLVED'),
        ('CLOSED', 'CLOSED'),
        ('OPEN', 'OPEN'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    incident_id = models.CharField(max_length=50, primary_key=True)
    priority = models.CharField(max_length=50)
    incident_type = models.CharField(max_length=250)
    incident_status = models.CharField(max_length=50, choices=STATUS)
    created_date = models.DateTimeField()
    resolution_date = models.DateTimeField()
    department = models.ForeignKey(Department, on_delete=CASCADE, null=True, blank=True)

    def __repr__(self):
        return self.incident_id
    
    def __str__(self):
        return self.incident_id


class ClosedIncident(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('RESOLVED', 'RESOLVED'),
        ('CLOSED', 'CLOSED'),
        ('OPEN', 'OPEN'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    incident_id = models.CharField(max_length=50, primary_key=True)
    priority = models.CharField(max_length=50)
    incident_type = models.CharField(max_length=250)
    incident_status = models.CharField(max_length=50, choices=STATUS)
    created_date = models.DateTimeField()
    resolution_date = models.DateTimeField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=CASCADE, null=True, blank=True)

    def __repr__(self):
        return self.incident_id
    
    def __str__(self):
        return self.incident_id


class BacklogIncident(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('RESOLVED', 'RESOLVED'),
        ('CLOSED', 'CLOSED'),
        ('OPEN', 'OPEN'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    incident_id = models.CharField(max_length=50, primary_key=True)
    priority = models.CharField(max_length=50)
    incident_type = models.CharField(max_length=250)
    incident_status = models.CharField(max_length=50, choices=STATUS)
    created_date = models.DateTimeField()
    resolution_date = models.DateTimeField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=CASCADE, null=True, blank=True)

    def __repr__(self):
        return self.incident_id
    
    def __str__(self):
        return self.incident_id


class CriticalIncident(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('RESOLVED', 'RESOLVED'),
        ('CLOSED', 'CLOSED'),
        ('OPEN', 'OPEN'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    incident_id = models.CharField(max_length=50, primary_key=True)
    priority = models.CharField(max_length=50)
    incident_status = models.CharField(max_length=50, choices=STATUS)
    created_date = models.DateTimeField()
    resolution_date = models.DateTimeField(null=True, blank=True)
    application = models.ForeignKey(CriticalService, on_delete=CASCADE, null=True, blank=True)

    def __repr__(self):
        return self.incident_id
    
    def __str__(self):
        return self.incident_id
