from django.db import models
from .enums import FileImportTypes
from program.enums import EnrollmentStatus
from django.contrib.auth.models import User    #MPR

import pandas as pd
import xlrd 
from program.models import Enrollment, Program, EnrollmentActivity, EnrollmentService
from client.models import Client, ClientAddress
import logging
logging.basicConfig(filename = 'MPRapp.log', level = logging.INFO)
from django.core.exceptions import MultipleObjectsReturned
from iep.models import ClientIEP, ClientIEPEnrollment
from datetime import date
from agency.models import Agency
from random import randint
from note.models import Note
import datetime
from django.db import transaction

class FileImport(models.Model):                                                                          #MPR
    ftype = models.CharField( max_length=32, blank=False, null=False, help_text='Excel File Type Import:', #MPR
                             choices=[(x.name, x.value) for x in FileImportTypes], default=FileImportTypes.MPR)                       #MPR
    file_path = models.CharField(max_length=200,blank=False, null=False,help_text='Path of file to be imported including the file name')   #MPR
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,help_text='User executing the import')                #MPR
    import_parameters = models.CharField(max_length=200,blank=True, null=True,help_text='parameters of the import is a dictionary stored as json.loads string')   #MPR
    period = models.CharField(max_length=36,blank=True, null=True,help_text='file upload period in weeks or months etc..')   #MPR
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, blank=True, null=True,help_text='Agency for which the import is executed, typically User\'s agency.')  
    result = models.CharField(max_length=500,blank=True, null=True,help_text='result of import job run stored as dictionary string')
    run_id = models.IntegerField(blank=True, null=True,help_text='Label of import job run stored as dictionary string')
    timestamp = models.DateTimeField(auto_now_add= True)
    
    def inspect(self):                                                                             #MPR
        # Inspect the input file for format validation                                             #MPR
        # Returns true if contents and the format is as expected, returns false otherwise          #MPR
        ## TODO: check that the first sheet's column names match the template's                    #MPR
        loc = (self.file_path) 
        try:
           wb = xlrd.open_workbook(loc) 
           sheet = wb.sheet_by_index(1) 
           provider=sheet.cell_value(2,0)
           month=sheet.cell_value(4,0)
        except IOError as e:
           return (False,'Error reading Excel file! '+str(e),None)
        return (True, "File Format is Valid", wb.sheet_names())                                                      #MPR

    def run_MPR(self):                                                                  #MPR
        ## MPR IMPORT SCRIPT
        ## Reads the input excel file contaning the Monthly Participation Report - MPR (e.g. MPR Provider1 2020Oct Sample.xlsx) 
        ## based on template in https://www.dropbox.com/sh/wklxg28lr3s3id6/AABXyIzSwd9AiFNCr16JdLzaa?dl=0 .
        ## Inserts each entry into SQL Database via Django model(that includes classes Client, ClientIEP, ClientIEPEnrollment, Program, Enrollment, EnrollmentActivity, EnrollmentService ).
        ## The MPR data is assumed to be in the second sheet. Any change in the template may result in unpredictable behaviour.
        ## Throws exceptions if file contains incomplete and\or invalid data.
        ## Provider is assumed to be in cell A3 and month in cell A5.    
        ## variable abbreviations\classes: c3=Client, a3=Agency, ciep3=ClientIEP, ciep_en3=ClientIEPEnrollment, e3=ciep_en3.enrollment, ea3=EnrollmentActivity, es3=EnrollmentService, n3=Note
        
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
           return ({'records read':0,'records inserted':0,'records failed':0,'error':'Error reading Excel file!'+str(e)}, None, None)
        if self.agency:
           a3=self.agency        
        else:
           a3,acreated=Agency.objects.get_or_create(name=provider)
        try:
            df['row_number'] = df.index + 12
            df['result'] = ''
            df.dropna(how = 'all',inplace=True)
            #df1=df.iloc[0:18,]   ## TODO use ix first rows to restrict number of records processed
            df1=df
            df1.rename(columns={'Unnamed: 15': 'Actual Attendance Week Hours'}, inplace=True)
        except Exception as ve:
            err3='Error possible unrecognized columns'
            print(err3 + str(ve))
            return ({'records read':0,'records inserted':0,'records failed':0,'error':str(ve) + err3}, None, None)        
        try:
            df1[' Client ID'].astype('Int64', copy=False)
            df1['Case Number'].astype('Int64', copy=False)
            df1['Qualifying Activity (51% or >) Hours'].astype('Int64', copy=False)
            df1['Non-Qualifying Activity (49% or <) Hours'].astype('Int64', copy=False)
            df1['Actual Attendance Week Hours'].astype('float', copy=False)
            df1['Required Number of Participation Hours\n(I+L)'].astype('Int64', copy=False)
        except (ValueError,KeyError) as ve:
            print(str(ve))
            err3='One of the following columns have an unexpected value: Client ID; Case Number;Qualifying Activity (51% or >) Hours;Non-Qualifying Activity (49% or <) Hours;Actual Attendance Week Hours;Required Number of Participation Hours\n(I+L)'
            print(err3)
            #return ({'records read':0,'records inserted':0,'records failed':0,'error':str(ve) + err3}, None, None)
        #print(df1)  ## TODO delete later
        # df1[pd.isnull(df1)]=None  # didn't work
        df1 = df1.where(pd.notnull(df1), None)
        print(df1.iloc[0])  ## TODO delete later
        print(df1.info())
        insert_count=0
        fail_count=0
        attempt_count=0
        data_import_batch_id=randint(1, 2000000000)
        for i in range(0, df1.shape[0]): # for each row in the excel file data section
          row = df1.iloc[i]
          ea3=None   #EnrollmentActivity 
          if not(pd.isnull(row['First Name'])) or not(pd.isnull(row['Last Name'])) or not(pd.isnull(row[' Client ID'])):   #if any one of them is non-null
            # par=participation(First_Name=row['First Name'],Last_Name=row['Last Name'],...)
            attempt_count+=1
            valid_row=True  # row with Actual Total Monthly Participation Hours value (Week 1). Others have null values.
            try:
              with transaction.atomic():
                c3=Client.objects.filter(snap_id=row[' Client ID']).first()
                if c3:
                   print('Client in the DB:' + str(c3.first_name) + ' ' + str(c3.last_name) + ' with pk=' + str(c3.id) )
                   if c3.address.county!=row['County of Residence']:
                      c3.address.county=row['County of Residence']
                      c3.address.save()
                else:
                   ca1=ClientAddress(county=row['County of Residence'])
                   c3=Client(first_name=row['First Name'],last_name=row['Last Name'],snap_id=row[' Client ID'],address=ca1)
                   ca1.save()
                   c3.save()
                   print('Created Client ' + str(c3.first_name) + ' ' + str(c3.last_name) + ' with pk=' + str(c3.id) )
                if Client.objects.filter(snap_id=row[' Client ID']).count()>1:
                   print('MultipleObjectsReturned for gsnap_id=' + str(c3.snap_id) + '. Picking the first one with pk=' + str(c3.pk))   
                   logging.exception('MultipleObjectsReturned for gsnap_id=' + str(c3.snap_id) + '. Picking the first one with pk=' + str(c3.pk))                   
                ## TODO: Do we update c3.address.county?             
                if c3.ieps.count():
                      ciep3=c3.ieps.filter(case_number=row['Case Number']).first()
                      if not ciep3:
                         ciep3=ClientIEP(client=c3, case_number=row['Case Number'],projected_end_date=None if pd.isnull(row['Projected End Date ']) else row['Projected End Date '].date())
                         print('Created ClientIEP with case number=' +  str(ciep3.case_number) + ' with pk=' + str(ciep3.id) )   
                      else:
                         print('Found ClientIEP with case_number=' + str(ciep3.case_number) )                  
                         ciep3.projected_end_date=None if pd.isnull(row['Projected End Date ']) else row['Projected End Date '].date()
                else:
                      ciep3=ClientIEP(client=c3, case_number=row['Case Number'],projected_end_date=None if pd.isnull(row['Projected End Date ']) else row['Projected End Date '].date())
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
                      e3=Enrollment(client=c3,program=p3,start_date=None if pd.isnull(row['Activity Enrollment Date']) else row['Activity Enrollment Date'].date(), end_date=None if pd.isnull(row['Date Participation Terminated']) else row['Date Participation Terminated'].date(), end_reason=row['Reason Participation Terminated'],status=EnrollmentStatus.ENROLLED.value)
                      e3.save()
                      ciep_en3.enrollment=e3
                      ciep_en3.save()
                #Create EnrollmentActivity
                ea3=EnrollmentActivity(enrollment=e3, 
                                       start_date=None if pd.isnull(row['Activity Enrollment Date']) else row['Activity Enrollment Date'].date(), 
                                       end_date=None if pd.isnull(row['Date Participation Terminated']) else row['Date Participation Terminated'].date(),
                                       qualifying_activity_name = row['Qualifying Activity Enrolled'],
                                       qualifying_activity_hours = row['Qualifying Activity (51% or >) Hours'],
                                       billable_activity = row['Is Qualifying Activity Billable (Y/N)'], non_qualifying_activity_hours = row['Non-Qualifying Activity (49% or <) Hours'], required_number_of_articipatio_hours = row['Required Number of Participation Hours\n(I+L)'], actual_total_monthly_participation_hours = row['Actual Total Monthly Participation Hours'],
                                       hours_met = row['Was ABAWD Work Requirement Met (Y/N)'],
                                       performance_met = row['Meeting Performance Standards (Y/N)'],
                                       month = month,
                                       sheet = sheet.name,
                                       provider = provider,
                                       data_import_id = str(data_import_batch_id))                                                            
                ea3.save()
                print('Enrollment Activity created')
                n1 = Note(source=ea3, text='' if pd.isnull(row['If not Meeting Performance Standards, Please Explain']) else row['If not Meeting Performance Standards, Please Explain'])
                n1.save()
                attendance_hours={row['Actual Attendance Week']:row['Actual Attendance Week Hours']} 
                if (ea3.id):
                   insert_count+=1
                   df1.at[i,'result']='Processed.'  
                else:
                   fail_count+=1
                   df1.at[i,'result']='Failed to insert Enrollment Activity.'  
                #Create EnrollmentService
                es3=EnrollmentService(enrollment=e3,
                                      offered=row['Support Service Offered (Y/N)'],
                                      type_and_amount=row['Support Service Issued (Type & Amount)'],
                                      if_no_support_services_needed_explain_why=row['If No Support Services Needed, Explain Why'],
                                      retention_services_type_amount=row['Retention Services Provided (Type & Amount)'],
                                      data_import_id=str(data_import_batch_id) )
                es3.save()
                n2 = Note(source=es3, text='' if pd.isnull(row['Comments']) else row['Comments'])
                n2.save()  
            except Exception as e:
               fail_count+=1
               print('Error at excel row number ' + str(row['row_number']) + ': ' + str(e))          
               df1.at[i,'result']='Error at excel row number ' + str(row['row_number']) + ': ' + str(e)
          else:  # if client data is null, Actual Attendance Week data gathered here (week1, week2 ..)
            try:
                if valid_row and ea3:
                   attendance_hours[row['Actual Attendance Week']]=row['Actual Attendance Week Hours']
                   if row['Actual Attendance Week']=='Week 5':
                      ea3.actual_attendance_week=str(attendance_hours)   # use eval function to convert string back to dictionary
                      ea3.save()  
                      valid_row=False  
            except Exception as e:
               print('Error at excel row number ' + str(row['row_number']) + ': ' + str(e))          
               df1.at[i,'result']='Error at excel row number ' + str(row['row_number']) + ': ' + str(e)
                    
        self.run_id=data_import_batch_id
        self.period=month
        run_result={'records read':attempt_count,'records inserted':insert_count,'records failed':fail_count}
        self.result=str(run_result)
        return (run_result, df1['row_number'].tolist(), df1['result'].tolist())
       
    def run(self):                                                                  #MPR
        # Run import script
        if self.ftype == FileImportTypes.MPR :
           (run_report, row_numbers, results) = self.run_MPR()
           self.save()
           return run_report, row_numbers, results           
            
