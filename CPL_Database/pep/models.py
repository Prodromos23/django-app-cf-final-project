from django.db import models
from CPL_Database.models import Fund,Subfund,Person_Reviewers,ServiceProviderType
# from CPL_Database.mixins import MultiDBSaveMixin

# todo: CREATE INDEXES FOR ALL FOREIGN KEYS

class PEP_Entities(models.Model):
    pep_entities_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    subfunds = models.ManyToManyField(Subfund,through='PEP_Entities_Subfund')

    class Meta:
        db_table = 'PEP_Entities'
        verbose_name = 'PEP Entity'
        verbose_name_plural = 'PEP Entities'

        indexes = [
            models.Index(fields=['entity_name']),
        ]


    def __str__(self):
        return self.entity_name

class PEP_Entities_Subfund(models.Model):
    pep_entities_subfund_id = models.AutoField(primary_key=True)
    entities_id_fk = models.ForeignKey(PEP_Entities, on_delete=models.CASCADE,null=True)
    subfund_id_fk = models.ForeignKey(Subfund, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PEP_Entities_Subfund'
        verbose_name = 'PEP Entities-Subfund'
        verbose_name_plural = 'PEP Entities Subfund'
    
        indexes = [
            models.Index(fields=['entities_id_fk']),
            models.Index(fields=['subfund_id_fk']),
        ]


    def __str__(self):
        return f'{self.entities_id_fk.entity_name} - {self.subfund_id_fk.subfund_name}'


class PEP_Names(models.Model):
    pep_names_id = models.AutoField(primary_key=True)
    pep_name = models.CharField(max_length=255, null=True,default="No Name")
    position = models.CharField(max_length=100, default="Unknown Position")
    # entities_id_fk = models.ForeignKey(PEP_Entities, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'PEP_Names'
        verbose_name = 'PEP Name'
        verbose_name_plural = 'PEP Names'

        indexes = [
            models.Index(fields=['pep_name']),
            models.Index(fields=['position']),
        ]


    def __str__(self):
        return self.pep_name or 'No Name'


class PEP_Entities_Names(models.Model):
    entities_names_id = models.AutoField(primary_key=True)
    entities_id_fk = models.ForeignKey(PEP_Entities, on_delete=models.CASCADE,null=True,blank=True)
    names_id_fk = models.ForeignKey(PEP_Names, on_delete=models.CASCADE)
    removed = models.BooleanField(default=False,help_text="0:No|1:Yes")

    class Meta:
        db_table = 'PEP_Entities_Names'
        verbose_name = 'PEP Entities-Names'
        verbose_name_plural = 'PEP Entities_Names'

        indexes = [
            models.Index(fields=['entities_id_fk']),
            models.Index(fields=['names_id_fk']),
        ]


    def __str__(self):
        return f'{self.entities_id_fk.entity_name} - {self.names_id_fk.pep_name}'
    

class PEP_Name_Screening(models.Model):
    pep_names_screening_id = models.AutoField(primary_key=True)
    result_type = models.CharField(max_length=50)
    # name_screened = models.CharField(max_length=255)

    class Meta:
        db_table = 'PEP_Name_Screening'
        verbose_name = 'PEP Name Screening'
        verbose_name_plural = 'PEP Name Screenings'

    def __str__(self):
        return f'{self.result_type}'

class PEP_Dates(models.Model):
    pep_dates_id = models.AutoField(primary_key=True)
    entities_names_id_fk = models.ForeignKey(PEP_Entities_Names, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    date_validation_rc = models.DateField(null=True,blank=True)
    date_approval_mc = models.DateField(null=True,blank=True)
    date_approval_brd = models.DateField(null=True,blank=True)
    date_removal = models.DateField(null=True,blank=True)
    date_updated_last = models.DateField(null=True,blank=True)

    class Meta:
        db_table = 'PEP_Dates'
        verbose_name = 'PEP Date'
        verbose_name_plural = 'PEP Dates'

        indexes = [
            models.Index(fields=['entities_names_id_fk']),
            models.Index(fields=['date_added']),
            models.Index(fields=['date_validation_rc']),
            models.Index(fields=['date_approval_mc']),
            models.Index(fields=['date_approval_brd']),
            models.Index(fields=['date_removal']),
            models.Index(fields=['date_updated_last']),
        ]


class PEP_Classifications(models.Model):
    pep_classifications_id = models.AutoField(primary_key=True)
    classification_status = models.CharField(max_length=150,null=False)

    class Meta:
        db_table = 'PEP_Classifications'
        verbose_name = 'PEP Classification'
        verbose_name_plural = 'PEP Classifications'

    def __str__(self):
        return f'{self.classification_status}'


class PEP_Estimations(models.Model):
    pep_estimations_id = models.AutoField(primary_key=True)
    estimation_status = models.CharField(max_length=150,null=False)

    class Meta:
        db_table = 'PEP_Estimations'
        verbose_name = 'PEP Estimation'
        verbose_name_plural = 'PEP Estimations'

    def __str__(self):
        return f'{self.estimation_status}'

class PEP_Nationality(models.Model):
    pep_nationality_id = models.AutoField(primary_key=True)
    nationality = models.CharField(max_length=200,null=False)

    class Meta:
        db_table = 'PEP_Nationality'
        verbose_name = 'PEP Nationality'
        verbose_name_plural = 'PEP Nationalities'
    
    def __str__(self):
        return f'{self.nationality}'

class PEP_Info(models.Model):
    pep_info_id = models.AutoField(primary_key=True)
    entities_names_id_fk = models.ForeignKey(PEP_Entities_Names, on_delete=models.CASCADE)
    pep_names_screening_id_fk = models.ForeignKey(PEP_Name_Screening, on_delete=models.CASCADE)
    comment_screening = models.TextField(null=True)
    comment_assessment = models.TextField(null=True)
    person_reviewers_id_fk = models.ForeignKey(Person_Reviewers, on_delete=models.CASCADE, related_name='person_reviewers')
    rc_validation_id_fk = models.ForeignKey(Person_Reviewers, on_delete=models.CASCADE,null=True, related_name='rc_validations')
    slamlux_classification_id_fk = models.ForeignKey(PEP_Classifications,on_delete=models.CASCADE,related_name='slamlux_classification')
    ta_classification_id_fk = models.ForeignKey(PEP_Classifications,on_delete=models.CASCADE,related_name='ta_classification')
    slamlux_estimation_id_fk = models.ForeignKey(PEP_Estimations,on_delete=models.CASCADE,related_name='slamlux_estimation')
    ta_estimation_id_fk = models.ForeignKey(PEP_Estimations,on_delete=models.CASCADE,related_name='ta_estimation')
    pep_nationality_id_fk = models.ForeignKey(PEP_Nationality,on_delete=models.CASCADE,related_name='location')
    pep_dates_id_fk = models.ForeignKey(PEP_Dates,on_delete=models.CASCADE,related_name='date')
    service_provider = models.ForeignKey(ServiceProviderType,on_delete=models.CASCADE,related_name='service_provider_type')
    is_rr_validated = models.BooleanField(null=True,help_text="0:No|1:Yes")
    comment_mc_board = models.TextField(null=True)
    pep_remove_reason = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'PEP_Info'
        verbose_name = 'PEP Info'
        verbose_name_plural = 'PEP Infos'

        indexes = [
            models.Index(fields=['entities_names_id_fk']),
            models.Index(fields=['pep_names_screening_id_fk']),
            models.Index(fields=['person_reviewers_id_fk']),
            models.Index(fields=['rc_validation_id_fk']),
            models.Index(fields=['slamlux_classification_id_fk']),
            models.Index(fields=['ta_classification_id_fk']),
            models.Index(fields=['slamlux_estimation_id_fk']),
            models.Index(fields=['ta_estimation_id_fk']),
            models.Index(fields=['pep_nationality_id_fk']),
            models.Index(fields=['pep_dates_id_fk']),
            models.Index(fields=['service_provider']),
        ]


    def __str__(self):
        return f'{self.entities_names_id_fk.entities_id_fk.entity_name} - {self.entities_names_id_fk.names_id_fk.pep_name}'


    def delete(self, *args, **kwargs):
        # Delete related PEP_Dates instances
        PEP_Dates.objects.filter(entities_names_id_fk=self.entities_names_id_fk).delete()
        # Delete related PEP_Entities_Names instances
        PEP_Entities_Names.objects.filter(entities_id_fk=self.entities_names_id_fk.entities_id_fk, names_id_fk=self.entities_names_id_fk.names_id_fk).delete()
        # Delete related PEP_Entities_Subfund instances
        PEP_Entities_Subfund.objects.filter(entities_id_fk=self.entities_names_id_fk.entities_id_fk).delete()
        super().delete(*args, **kwargs)



