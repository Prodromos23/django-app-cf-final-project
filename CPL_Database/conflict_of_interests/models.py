from django.db import models
from CPL_Database.models import Subfund
# from CPL_Database.mixins import MultiDBSaveMixin
# todo: CREATE INDEXES FOR ALL FOREIGN KEYS

class COI_Cases(models.Model):
    coi_cases_id = models.AutoField(primary_key=True)
    area_of_conflict = models.CharField(max_length=150)
    event_description = models.TextField(null=True)
    removed = models.BooleanField(default=False,help_text="0:No|1:Yes")
    subfunds = models.ManyToManyField(Subfund,through='COI_Cases_Subfund')

    class Meta:
        db_table = 'COI_Cases'
        verbose_name = 'COI Case'
        verbose_name_plural = 'COI Cases'

        indexes = [
            models.Index(fields=['area_of_conflict']),
        ]

    def __str__(self):
        return self.area_of_conflict

class COI_Cases_Subfund(models.Model):
    coi_cases_subfund_id = models.AutoField(primary_key=True)
    cases_id_fk = models.ForeignKey(COI_Cases, on_delete=models.CASCADE,null=True)
    subfund_id_fk = models.ForeignKey(Subfund, on_delete=models.CASCADE)

    class Meta:
        db_table = 'COI_Cases_Subfund'
        verbose_name = 'COI Cases-Subfund'
        verbose_name_plural = 'COI Cases Subfund'


        indexes = [
            models.Index(fields=['cases_id_fk']),
            models.Index(fields=['subfund_id_fk']),
        ]

    
    def __str__(self):
        return f'{self.cases_id_fk.area_of_conflict} - {self.subfund_id_fk.subfund_name}'

class COI_Dates(models.Model):
    coi_dates_id = models.AutoField(primary_key=True)
    cases_id_fk = models.ForeignKey(COI_Cases, on_delete=models.CASCADE,verbose_name="Case")
    date_added = models.DateField(auto_now_add=True)
    date_review_mc = models.DateField(null=True,blank=True)
    date_review_brd = models.DateField(null=True,blank=True)
    date_removal = models.DateField(null=True,blank=True)
    date_updated_last = models.DateField(null=True,blank=True)

    class Meta:
        db_table = 'COI_Dates'
        verbose_name = 'COI Date'
        verbose_name_plural = 'COI Dates'

        indexes = [
            models.Index(fields=['cases_id_fk']),
            models.Index(fields=['date_added']),
            models.Index(fields=['date_review_mc']),
            models.Index(fields=['date_review_brd']),
            models.Index(fields=['date_removal']),
            models.Index(fields=['date_updated_last']),
        ]


    def __str__(self):
        return f'{self.cases_id_fk.area_of_conflict}'

class COI_Status(models.Model):
    coi_status_id = models.AutoField(primary_key=True)
    status_description = models.CharField(max_length=255)

    class Meta:
        db_table = 'COI_Status'
        verbose_name = 'COI Status'
        verbose_name_plural = 'COI Status'

    def __str__(self):
        return self.status_description
    

class COI_Info(models.Model):
    coi_info_id = models.AutoField(primary_key=True)
    cases_id_fk = models.ForeignKey(COI_Cases, on_delete=models.CASCADE, related_name='info',verbose_name="Cases")  # New foreign key to COI_Cases
    isProven = models.BooleanField(help_text= "0:Theoretical|1:Proven")
    unit = models.TextField(null=True)
    mitigation_measures = models.TextField(null=True)
    isInvestorInformed = models.BooleanField(help_text= "0:Theoretical|1:Proven",verbose_name="Is Investor Informed")
    status_id_fk = models.ForeignKey(COI_Status,on_delete=models.CASCADE,related_name="status",verbose_name="Status")
    coi_dates_id_fk = models.ForeignKey(COI_Dates,on_delete=models.CASCADE,related_name='date')

    class Meta:
        db_table = 'COI_Info'
        verbose_name = 'COI Info'
        verbose_name_plural = 'COI Infos'
    
        indexes = [
            models.Index(fields=['cases_id_fk']),
            models.Index(fields=['status_id_fk']),
            models.Index(fields=['coi_dates_id_fk']),
        ]


    def __str__(self):
        return f'Info for {self.coi_dates_id_fk.cases_id_fk.area_of_conflict}'

