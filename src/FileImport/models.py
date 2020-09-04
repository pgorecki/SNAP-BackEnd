from django.db import models
from .enums import FileImportTypes
from django.contrib.auth.models import User    #MPR

import pandas as pd
import xlrd 
from program.models import Enrollment
from client.models import Client, ClientAddress
import logging
logging.basicConfig(filename = 'MPRapp.log', level = logging.INFO)
from django.core.exceptions import MultipleObjectsReturned

class FileImport(models.Model):                                                                          #MPR
    ftype = models.CharField( max_length=32, blank=False, null=False, help_text='Excel File Type Import:', #MPR
                             choices=[(x.name, x.value) for x in FileImportTypes], default=FileImportTypes.MPR)                       #MPR
    file_path = models.CharField(max_length=200,blank=False, null=False,help_text='Path of file to be imported including the file name')   #MPR
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,help_text='User executing the import')                #MPR
    import_parameters = models.CharField(max_length=200,blank=True, null=True,help_text='parameters of the import is a dictionary stored as json.loads string')   #MPR
    period = models.CharField(max_length=36,blank=True, null=True,help_text='file upload period in weeks or months etc..')   #MPR
    
    def inspect(self):                                                                             #MPR
        # Inspect the input file for format validation                                             #MPR
        # Returns true if contents and the format is as expected, returns false otherwise          #MPR
        ## TODO: check that the column names match the templates'                                  #MPR
        return (True, "File Format is Valid")                                                      #MPR

    def run_MPR(self):                                                                  #MPR
        ## MPR IMPORT SCRIPT
        ## Reads the input excel file contaning the Monthly Participation Report - MPR (e.g. MPR Provider1 2020Oct Sample.xlsx) 
        ## based on template in https://www.dropbox.com/sh/wklxg28lr3s3id6/AABXyIzSwd9AiFNCr16JdLzaa?dl=0 .
        ## Inserts each entry into SQL Database thru Django model(participation class).
        ## The MPR data is assumed to be in the second sheet. Any change in the template may result in unpredictable behaviour.
        ## Provider is assumed to be in cell A3 and month in cell A5.    
        # TODO: Input Parameter: Mapping between file columns and Class fields including the index?
        # TODO: Add created_date field
        # TODO: Add exception handling
        # TODO: Return # entries processed
        print('Running MPR Import Script')
        loc = (self.file_path) 
        try:
           wb = xlrd.open_workbook(loc) 
           sheet = wb.sheet_by_index(1) 
           provider=sheet.cell_value(2,0)
           month=sheet.cell_value(4,0)
           df = pd.read_excel(self.file_path, sheet_name=1, header=10)
        except IOError as e:
           logging.exception(str(e))
           return (0,0,0,'Error reading excel file!')       
        df.dropna(how = 'all',inplace=True)
        print(df.columns.values)
        df1=df.iloc[0:18,]   ## TODO use ix first rows to restrict number of records processed
        df1.rename(columns={'Unnamed: 15': 'Actual Attendance Week Hours'}, inplace=True)
        print(df1)  ## TODO delete later
        insert_count=0
        fail_count=0
        attempt_count=0
        for i in range(0, df1.shape[0]): # for each row in the excel file data section
          row = df1.iloc[i]
          if not(pd.isnull(row['First Name'])) or not(pd.isnull(row['Last Name'])) or not(pd.isnull(row[' Client ID'])):   #if any one of them is non-null
            # save record
            # par=participation(First_Name=row['First Name'],Last_Name=row['Last Name'],...)
            try:
               c3=Client.objects.get(snap_id=row[' Client ID'])
            except MultipleObjectsReturned:
               print('MultipleObjectsReturned . Picking the first one.')
               c3=Client.objects.filter(snap_id=row[' Client ID']).first()  
            except Client.DoesNotExist:
               print('Client Does not exits. Create One') 
               ca1=ClientAddress(county=row['County of Residence'])
               c3=Client(first_name=row['First Name'],last_name=row['Last Name'],snap_id=row[' Client ID'],address=ca1)
            attempt_count+=1
            ca1.save()
            c3.save()
            if (c3.id):
               insert_count+=1
            else:
               fail_count+=1
        return (attempt_count,insert_count,fail_count)

        
    def run(self):                                                                  #MPR
        # Run import script
        if self.ftype == FileImportTypes.MPR :
           self.run_MPR()
        return    
