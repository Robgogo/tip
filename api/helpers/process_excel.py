# TODO: Implement excel transformation to JSON and upload.
import pandas as pd
import csv
import os

from api.models.incidents import RaisedIncident, ClosedIncident, BacklogIncident, CriticalIncident, Department, CriticalService


def critical_incidents_excel_handler(filename):
    try:
        data = pd.read_excel(filename)
        incident_df = data[['Incident ID', 'Date raised', 'Date closed', 'Priority', 'Status', 'CI Name']]
        bulk_creator = []
        for idx, row in incident_df.iterrows():
            application = CriticalService.objects.filter(application=row['CI Name']).first()
            new_inc = CriticalIncident(incident_id=row['Incident ID'], created_date=row['Date raised'],
                                       resolution_date=row['Date closed'], priority=row['Priority'], incident_status=row['Status'],
                                       application=application)
            bulk_creator.append(new_inc)
        CriticalIncident.objects.bulk_create(bulk_creator)
        new_filename = filename.split('.')[0]
        incident_df.to_csv(new_filename + '.csv')
        # TODO: gcloud storage upload here
        return "Success"
    except Exception as e:
        return "Failed"


def raised_incidents_excel_handler(filename):
    return NotImplemented


def closed_incidents_excel_handler(filename):
    return NotImplemented


def backlog_incidents_excel_handler(filename):
    return NotImplemented
