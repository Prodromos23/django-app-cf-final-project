from django.db import models
# from CPL_Database.mixins import MultiDBSaveMixin

class Fund(models.Model):
    fund_id = models.IntegerField(primary_key=True)
    fund_name = models.CharField(max_length=50)
    fund_status_id_fk = models.CharField(max_length=50)

    class Meta:
        db_table = 'FUND'
        verbose_name = 'Fund'
        verbose_name_plural = 'Funds'

        indexes = [
            models.Index(fields=['fund_name']),
            models.Index(fields=['fund_status_id_fk']),
        ]

    def __str__(self):
        return self.fund_name

class Subfund(models.Model):
    subfund_id = models.IntegerField(primary_key=True)
    fund_id_fk = models.ForeignKey(Fund, on_delete = models.CASCADE,verbose_name="Fund")
    subfund_name = models.CharField(max_length=100)
    is_subfund = models.BooleanField(help_text="0:No|1:Yes")
    is_umbrella = models.BooleanField(help_text="0:No|1:Yes")

    class Meta:
        db_table = 'SUBFUND'
        verbose_name = 'Subfund'
        verbose_name_plural = 'Subfunds'


        indexes = [
            models.Index(fields=['fund_id_fk']),
            models.Index(fields=['subfund_name']),
        ]


    def __str__(self):
        return self.subfund_name


class Person_Reviewers(models.Model):
    person_id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    person_email = models.CharField(max_length=100)
    slfm_department_compliance_id = models.IntegerField()
    slfm_department_name = models.CharField(max_length=100)
    sub_department_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Person_Reviewers'
        verbose_name = 'Person Reviewer'
        verbose_name_plural = 'Person Reviewers'

    indexes = [
        models.Index(fields=['lastname']),
        models.Index(fields=['firstname']),
        models.Index(fields=['person_email']),
    ]

    def __str__(self):
        return f'{self.lastname} {self.firstname}'
    

class ServiceProviderType(models.Model):
    service_provider_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=150)

    class Meta:
        db_table = 'SERVICE_PROVIDER_TYPE'
        verbose_name = 'Service Provider Type'
        verbose_name_plural = 'Service Provider Types'

        indexes = [
            models.Index(fields=['type']),
        ]


    def __str__(self):
        return f'{self.type}'