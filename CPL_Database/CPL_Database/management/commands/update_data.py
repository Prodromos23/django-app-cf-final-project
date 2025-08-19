from django.core.management.base import BaseCommand
from ...db_connection.db_connection import DataBase_Connection
from django.utils.dateparse import parse_date
from CPL_Database.models import Fund,Subfund,ServiceProviderType,Person_Reviewers
from .command_utils import *

class Command(BaseCommand):
    '''
    Command Class to load data from the local Database
    '''
    help = 'Fetch and update data from external database'

    def handle(self, *args, **kwargs):
        self.clear_tables()
        self.load_fund_data()
        self.load_subfund_data()
        self.load_service_provider_data()
        self.load_person_reviewers_data()
        self.stdout.write(self.style.SUCCESS('Successfully updated data'))

    def clear_tables(self):
        Fund.objects.all().delete()
        Subfund.objects.all().delete()
        ServiceProviderType.objects.all().delete()
        Person_Reviewers.objects.all().delete()

    def load_fund_data(self):
        df1 = DataBase_Connection().execute_query_to_df(query="SELECT * FROM FUND;")[["FUND_ID","FUND_NAME","FUND_STATUS_ID_FK"]]
        df1.rename(columns={"FUND_ID":"fund_id","FUND_NAME":"fund_name","FUND_STATUS_ID_FK":"fund_status_id_fk"}, inplace=True)
        load_data_from_dataframe(df1, Fund)

    def load_subfund_data(self):
        df2 = DataBase_Connection().execute_query_to_df(query="SELECT * FROM SUBFUND;")[["SUBFUND_ID","FUND_ID_FK","SUBFUND_NAME","IS_SUBFUND","IS_UMBRELLA"]]
        df2.rename(columns={"SUBFUND_ID":"subfund_id","FUND_ID_FK":"fund_id_fk","SUBFUND_NAME":"subfund_name","IS_SUBFUND":"is_subfund","IS_UMBRELLA":"is_umbrella"}, inplace=True)

        for index, row in df2.iterrows():
            fund_instance = Fund.objects.get(fund_id=row['fund_id_fk'])
            Subfund.objects.create(
                subfund_id=row['subfund_id'],
                fund_id_fk=fund_instance,
                subfund_name=row['subfund_name'],
                is_subfund=row['is_subfund'],
                is_umbrella=row['is_umbrella']
            )

    def load_service_provider_data(self):
        df3 = DataBase_Connection().execute_query_to_df(query="SELECT * FROM SERVICE_PROVIDER_TYPE;")
        df3.rename(columns={"SERVICE_PROVIDER_TYPE_ID":"service_provider_type_id","TYPE":"type"}, inplace=True)
        load_data_from_dataframe(df3, ServiceProviderType)

    def load_person_reviewers_data(self):
        # query = "SELECT * FROM PERSON left join SLFM_DEPARTMENT as dep on PERSON.DEPARTMENT_ID_FK = dep.SLFM_DEPARTMENT_ID where SUB_DEPARTMENT_NAME = 'Compliance' and LEAVE_DATE is null and PERSON_EMAIL not like '%.ext%';"
        query = "SELECT * FROM PERSON left join SLFM_DEPARTMENT as dep on PERSON.DEPARTMENT_ID_FK = dep.SLFM_DEPARTMENT_ID where SUB_DEPARTMENT_NAME = 'Compliance'  and PERSON_EMAIL not like '%.ext%'"
        df4 = DataBase_Connection().execute_query_to_df(query=query)[["PERSON_ID","LASTNAME","FIRSTNAME","PERSON_EMAIL","SLFM_DEPARTMENT_COMPLIANCE_ID","SLFM_DEPARTMENT_NAME","SUB_DEPARTMENT_NAME"]]
        df4.rename(columns={"PERSON_ID":"person_id","LASTNAME":"lastname",
                            "FIRSTNAME":"firstname","PERSON_EMAIL":"person_email","SLFM_DEPARTMENT_COMPLIANCE_ID":"slfm_department_compliance_id","SLFM_DEPARTMENT_NAME":"slfm_department_name","SUB_DEPARTMENT_NAME":"sub_department_name"}, inplace=True)
        load_data_from_dataframe(df4, Person_Reviewers)




