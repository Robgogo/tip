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
            created = row['Date raised'].to_pydatetime()
            resolved = row['Date closed'].to_pydatetime()
            new_inc = CriticalIncident(incident_id=row['Incident ID'], created_date=created,
                                       resolution_date=resolved, priority=row['Priority'], incident_status=row['Status'],
                                       application=application)
            bulk_creator.append(new_inc)
        CriticalIncident.objects.bulk_create(bulk_creator)
        new_filename = filename.split('.')[0]
        incident_df.to_csv(new_filename + '.csv')
        # TODO: gcloud storage upload here
        return "Success"
    except Exception as e:
        return "Failed"


def clear_empty_rows(data, num_rows):
    return data.drop(range(num_rows))


def sort_by_ccg(data):
    if 'Customer Company Group' in data:
        return data['Customer Company Group'] == 'IBERIA'
    return True


def sort_by_cc(data):
    return data['Customer Company'] == 'IBERIA'


def raised_incidents_excel_handler(filename):
    try:
        excel_file = pd.ExcelFile(filename)
        data = pd.read_excel(excel_file, sheet_name='MONTHLY INCIDENTS RAISED')
        data = clear_empty_rows(data, 17)
        headers = data.iloc[0]
        data = data[1:]
        data.columns = headers
        data = data[sort_by_ccg]
        data = data[sort_by_cc]
        data = data[['Incidenct Code', 'Create Date-Time', 'Resolution Date-Time', 'Incident Status', 'Priority', 'Inc. Type', 'Departamento Cliente']]
        bulk_creator = []
        for idx, row in data.iterrows():
            code = None
            if not type(row['Departamento Cliente']) == float:
                code = row['Departamento Cliente'].split('(')[1].split(')')[0]
                department = Department.objects.filter(department_code=code).first()
            created = row['Create Date-Time'].to_pydatetime()
            resolved = row['Resolution Date-Time'].to_pydatetime()
            new_raised = RaisedIncident(incident_id=row['Incidenct Code'], priority=row['Priority'], incident_type=row['Inc. Type'],
                                        incident_status=row['Incident Status'], created_date=created, resolution_date=resolved, department=department)
            bulk_creator.append(new_raised)
        RaisedIncident.objects.bulk_create(bulk_creator)
        month = filename.split('.')[0].split('-')[1]
        new_filename = f'monthly_incidents_raised-{month}.csv'
        data.to_csv(new_filename)
        # TODO: gcloud storage upload here
        return "Success"
    except Exception as e:
        return "Failed"  


def closed_incidents_excel_handler(filename):
    try:
        excel_file = pd.ExcelFile(filename)
        data = pd.read_excel(excel_file, sheet_name='MONTHLY INCIDENTS CLOSED')
        data = clear_empty_rows(data, 17)
        headers = data.iloc[0]
        data = data[1:]
        data.columns = headers
        data = data[sort_by_cc]
        data = data[['Incidenct Code', 'Creation Date-Time', 'Resolution Date-Time', 'Incident Status', 'Priority', 'Inc. Type', 'Departamento Cliente']]
        bulk_creator = []
        for idx, row in data.iterrows():
            code = None
            if not type(row['Departamento Cliente']) == float:
                code = row['Departamento Cliente'].split('(')[1].split(')')[0]
                department = Department.objects.filter(department_code=code).first()
            created = row['Create Date-Time'].to_pydatetime()
            resolved = row['Resolution Date-Time'].to_pydatetime()
            new_raised = RaisedIncident(incident_id=row['Incidenct Code'], priority=row['Priority'], incident_type=row['Inc. Type'],
                                        incident_status=row['Incident Status'], created_date=created, resolution_date=resolved, department=department)
            bulk_creator.append(new_raised)
        RaisedIncident.objects.bulk_create(bulk_creator)
        month = filename.split('.')[0].split('-')[1]
        new_filename = f'monthly_incidents_raised-{month}.csv'
        data.to_csv(new_filename)
        # TODO: gcloud storage upload here
        return "Success"
    except Exception as e:
        return "Failed"


def backlog_incidents_excel_handler(filename):
    try:
        excel_file = pd.ExcelFile(filename)
        data = pd.read_excel(excel_file, sheet_name='MONTHLY INCIDENTS BACKLOG')
        data = clear_empty_rows(data, 13)
        headers = data.iloc[0]
        data = data[1:]
        data.columns = headers
        data = data[sort_by_ccg]
        data = data[sort_by_cc]
        data = data[['Incidenct Code', 'Create Date-Time', 'Resolution Date-Time', 'Incident Status', 'Priority', 'Inc. Type', 'Departamento Cliente']]
        bulk_creator = []
        for idx, row in data.iterrows():
            code = None
            if not type(row['Departamento Cliente']) == float:
                code = row['Departamento Cliente'].split('(')[1].split(')')[0]
                department = Department.objects.filter(department_code=code).first()
            created = row['Creation Date-Time'].to_pydatetime()
            resolved = row['Resolution Date-Time'].to_pydatetime()
            # TODO: check if the incident exist before adding it to db
            new_raised = RaisedIncident(incident_id=row['Incidenct Code'], priority=row['Priority'], incident_type=row['Inc. Type'],
                                        incident_status=row['Incident Status'], created_date=created, resolution_date=resolved, department=department)
            bulk_creator.append(new_raised)
        RaisedIncident.objects.bulk_create(bulk_creator)
        month = filename.split('.')[0].split('-')[1]
        new_filename = f'monthly_incidents_raised-{month}.csv'
        data.to_csv(new_filename)
        # TODO: gcloud storage upload here
        return "Success"
    except Exception as e:
        return "Failed"  
