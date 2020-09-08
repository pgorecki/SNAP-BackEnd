from django.db import models
from .enums import FileImportTypes
from program.enums import EnrollmentStatus
from django.contrib.auth.models import User    #MPR

import pandas as pd
import xlrd 
from program.models import Enrollment, Program
from client.models import Client, ClientAddress
import logging
logging.basicConfig(filename = 'MPRapp.log', level = logging.INFO)
from django.core.exceptions import MultipleObjectsReturned
from iep.models import ClientIEP
from datetime import date
from agency.models import Agency

class FileImport(models.Model):                                                                          #MPR
    ftype = models.CharField( max_length=32, blank=False, null=False, help_text='Excel File Type Import:', #MPR
                             choices=[(x.name, x.value) for x in FileImportTypes], default=FileImportTypes.MPR)                       #MPR
    file_path = models.CharField(max_length=200,blank=False, null=False,help_text='Path of file to be imported including the file name')   #MPR
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,help_text='User executing the import')                #MPR
    import_parameters = models.CharField(max_length=200,blank=True, null=True,help_text='parameters of the import is a dictionary stored as json.loads string')   #MPR
    period = models.CharField(max_length=36,blank=True, null=True,help_text='file upload period in weeks or months etc..')   #MPR
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, blank=True, null=True,help_text='Agency for which the import is executed, typically User\'s agency.')  
    
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
        a3=Agency.objects.get_or_create(name=provider)
        df.dropna(how = 'all',inplace=True)
        print(df.columns.values)
        df1=df.iloc[0:18,]   ## TODO use ix first rows to restrict number of records processed
        df1.rename(columns={'Unnamed: 15': 'Actual Attendance Week Hours'}, inplace=True)
        df1[' Client ID'].astype('Int64', copy=False)
        df1['Case Number'].astype('Int64', copy=False)
        #print(df1)  ## TODO delete later
        print(df1.info())
        insert_count=0
        fail_count=0
        attempt_count=0
        for i in range(0, df1.shape[0]): # for each row in the excel file data section
          row = df1.iloc[i]
          if not(pd.isnull(row['First Name'])) or not(pd.isnull(row['Last Name'])) or not(pd.isnull(row[' Client ID'])):   #if any one of them is non-null
            # par=participation(First_Name=row['First Name'],Last_Name=row['Last Name'],...)
            try:
               c3=Client.objects.get(snap_id=row[' Client ID'])
               print('Client in the DB:' + str(c3.first_name) + ' ' + str(c3.last_name) + ' with pk=' + str(c3.id) )
               if c3.address.county!=row['County of Residence']:
                  c3.address.county=row['County of Residence']
                  c3.address.save()
            except Client.DoesNotExist:
               ca1=ClientAddress(county=row['County of Residence'])
               c3=Client(first_name=row['First Name'],last_name=row['Last Name'],snap_id=row[' Client ID'],address=ca1)
               ca1.save()
               c3.save()
               print('Created Client' + str(c3.first_name) + ' ' + str(c3.last_name) + ' with pk=' + str(c3.id) )
            except MultipleObjectsReturned:
               c3=Client.objects.filter(snap_id=row[' Client ID']).first() 
               print('MultipleObjectsReturned for gsnap_id=' + str(c3.snap_id) + '. Picking the first one with pk=' + str(c3.pk))     
            ## TODO: Do we update c3.address.county?             
            if c3.ieps.count():
                  ciep3=c3.ieps.filter(case_number=row['Case Number']).first()
                  if not ciep3:
                     ciep3=ClientIEP(client=c3, case_number=row['Case Number'],projected_end_date=row['Projected End Date '].date())
                     print('Created ClientIEP with case number=' +  str(ciep3.case_number) + ' with pk=' + str(ciep3.id) )   
                  else:
                     print('Found ClientIEP with case_number=' + str(ciep3.case_number) )                  
                     ciep3.projected_end_date=row['Projected End Date '].date()
            else:
                  ciep3=ClientIEP(client=c3, case_number=row['Case Number'],projected_end_date=row['Projected End Date '].date())
                  print('Created ClientIEP with case number=' +  str(ciep3.case_number) + ' with pk=' + str(ciep3.id) )                
            ciep3.save()                  
            if ciep3.iep_enrollments.count():
                  ciep_en3=ciep3.iep_enrollments.first()
            else:
                  ciep_en3=ClientIEPEnrollment(iep=ciep3)
                  ciep_en3.save()
            if ciep_en3.enrollment and ciep_en3.enrollment.start_date == row['Activity Enrollment Date'].date():
                  print('Enrollment exists')
                  e3=ciep_en3.enrollment
                  e3.end_date=row['Date Participation Terminated'].date()
                  e3.end_reason=row['Reason Participation Terminated']
                  e3.save()
            else:
                  print('Creating enrollment object')
                  p3=Program.objects.filter(name=row['Qualifying Activity Enrolled']).first()
                  if not p3:
                     print('Creating program')
                     p3=Program(name=row['Qualifying Activity Enrolled'],agency=a3)
                     p3.save()
                  e3=Enrollment(client=c3,program=p3,start_date=row['Activity Enrollment Date'].date(), end_date=row['Date Participation Terminated'].date(), end_reason=row['Reason Participation Terminated'],status=EnrollmentStatus.ENROLLED.value)
                  e3.save()
                  ciep_en3.enrollment=e3
                  ciep_en3.save()

                  
                         
                      
            # try:
               # ciep3=ClientIEP.objects.get(case_number=row['Case Number'])
               # print('IEPClient in the DB: with pk=' + str(ciep3.id) )
            # except ClientIEP.DoesNotExist:
               # ciep3=ClientIEP(client=c3, case_number=row['Case Number'])
               # ciep3.save()
               # print('Created Client' + str(c3.first_name) + ' ' + str(c3.last_name) + ' with pk=' + str(c3.id) )
            # except MultipleObjectsReturned:
               # ciep3=ClientIEP.objects.filter(case_number=row['Case Number']).first() 
               # print('MultipleObjectsReturned for Case Number=' + str(ciep3.case_number) + '. Picking the first one with pk=' + str(ciep3.pk))    
 
   #if Case Number does not exist:
   #   iep1=create ClientIEP(Case Number, Projected End Date,  ABAWD (Y/N) )
   #else:
   #   iep1= get ClientIEP(Case Number)

           
            attempt_count+=1
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
