from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from CPL_Database.models import Fund,Subfund,ServiceProviderType,Person_Reviewers
from pep.models import  PEP_Estimations, PEP_Classifications,PEP_Names,PEP_Name_Screening,PEP_Nationality,PEP_Entities,PEP_Entities_Names,PEP_Dates, PEP_Info,PEP_Entities_Subfund
from conflict_of_interests.models import COI_Cases, COI_Cases_Subfund, COI_Dates, COI_Status, COI_Info
import csv
import pandas as pd

def load_data_from_dataframe_with_mapping(df, model, field_mapping):
    for index, row in df.iterrows():
        model.objects.create(**{field: row[column] for column, field in field_mapping.items()})

def load_data_from_dataframe(df, model):
    for index, row in df.iterrows():
        model.objects.create(**row.to_dict())

class Command(BaseCommand):
    help = 'Load initial data from CSV files into the database'

    def load_fund_data(self):
        fund_data = pd.DataFrame([
            {"fund_id": 101, "fund_name": "Alpha Growth Fund", "fund_status_id_fk": 1},
            {"fund_id": 102, "fund_name": "Alpha Growth Fund1", "fund_status_id_fk": 2},
            {"fund_id": 103, "fund_name": "Gamma Equity Fund", "fund_status_id_fk": 1},
        ])
        load_data_from_dataframe(fund_data, Fund)
        # for _, row in fund_data.iterrows():
        #     Fund.objects.create(**row)

    def load_subfund_data(self):
        subfund_data = pd.DataFrame([
            {"subfund_id": 201, "fund_id_fk": 101, "subfund_name": "Funds (LUX) - Equity ESG Global High Dividend", "is_subfund": True, "is_umbrella": False},
            {"subfund_id": 202, "fund_id_fk": 101, "subfund_name": "Funds (LUX) - Bond ESG Global Corporates", "is_subfund": True, "is_umbrella": False},
            {"subfund_id": 203, "fund_id_fk": 102, "subfund_name": "Alpha Sub B", "is_subfund": False, "is_umbrella": True},
        ])
        for _, row in subfund_data.iterrows():
            fund_instance = Fund.objects.get(fund_id=row['fund_id_fk'])
            Subfund.objects.create(
                subfund_id=row['subfund_id'],
                fund_id_fk=fund_instance,
                subfund_name=row['subfund_name'],
                is_subfund=row['is_subfund'],
                is_umbrella=row['is_umbrella']
            )

    def load_service_provider_data(self):
        service_provider_data = pd.DataFrame([
            {"service_provider_type_id": 1, "type": "Administrator"},
            {"service_provider_type_id": 2, "type": "Custodian"},
            {"service_provider_type_id": 3, "type": "Auditor"},
        ])
        load_data_from_dataframe(service_provider_data, ServiceProviderType)
        # for _, row in service_provider_data.iterrows():
        #     ServiceProviderType.objects.create(**row)

    def load_person_reviewers_data(self):
        person_reviewers_data = pd.DataFrame([
            {
                "person_id": 1,
                "lastname": "Papadopoulou",
                "firstname": "Aikaterini",
                "person_email": "anna.smith@company.com",
                "slfm_department_compliance_id": 9,
                "slfm_department_name": "Risk & Compliance",
                "sub_department_name": "Compliance"
            },
            {
                "person_id": 2,
                "lastname": "G",
                "firstname": "Miriam",
                "person_email": "mark.G@company.com",
                "slfm_department_compliance_id": 9,
                "slfm_department_name": "Risk & Compliance",
                "sub_department_name": "Compliance"
            },
            {
                "person_id": 3,
                "lastname": "Lee",
                "firstname": "Sophie",
                "person_email": "sophie.lee@company.com",
                "slfm_department_compliance_id": 9,
                "slfm_department_name": "Risk & Compliance",
                "sub_department_name": "Compliance"
            },
        ])
        # for _, row in person_reviewers_data.iterrows():
        #     Person_Reviewers.objects.create(**row)
        load_data_from_dataframe(person_reviewers_data, Person_Reviewers)

    def load_pep_estimations_data(self):
        data = [
            ('High'),
            ('Medium High'),
            ('Medium'),
            ('Medium Low'),
            ('Low')
        ]
        estimations = [PEP_Estimations(estimation_status=es) for es in data]
        PEP_Estimations.objects.bulk_create(estimations)

    def load_pep_classifications_data(self):
        data = [
            ('Material'),
            ('Non-Material')
        ]
        classifications = [PEP_Classifications(classification_status=es) for es in data]
        PEP_Classifications.objects.bulk_create(classifications)

    def load_pep_names_data(self):
        PEP_Names.objects.get_or_create(
            pep_name="No Name",
            position=""
        )

    def load_pep_name_screening_data(self):
        data = [
            ('PEP'),
            ('SOE'),
            ('SIE'),
            ('RCA'),
            ('No Match')
        ]
        name_screening = [PEP_Name_Screening(result_type=es) for es in data]
        PEP_Name_Screening.objects.bulk_create(name_screening)

    def load_pep_nationality_data(self):
        data = [
            ('Domestic'),
            ('Foreign'),
            ('Senior function in intern and/or supranational organisations')
        ]
        nationality = [PEP_Nationality(nationality=es) for es in data]
        PEP_Nationality.objects.bulk_create(nationality)

    def add_initial_pep_data(self):
        # Define the CSV data
        csv_data = """PEP Info ID,Entity Name,PEP Name,Reviewer Name,RC Validator Name,Slamlux Classification,TA Classification,Slamlux Estimation,TA Estimation,Nationality,Position,Date Added,Date RC Validation,Date Approval MC,Date Approval Board,Date Updated,Comment Screening,Comment Assessment,Comment MC Board,PEP Remove Reason,Fund Name,Subfund Name,Service Provider Type
        1,Entity1,Name1,G Miriam,Papadopoulou Aikaterini,Non-Material,Material,Medium Low,High,Domestic,Position,2025-03-14,2025-03-14,2025-03-14,2025-03-14,,ASDFG,adfADF,adsfaSDF,,Alpha Growth Fund,Funds (LUX) - Equity ESG Global High Dividend,Advisor
        2,Entity2,Name2,Papadopoulou Aikaterini,Papadopoulou Aikaterini,Non-Material,Material,Medium Low,High,Domestic,Position,2025-03-14,2025-03-14,2025-03-14,2025-03-14,,ASDFG,adfADF,adsfaSDF,,Alpha Growth Fund,Funds (LUX) - Equity ESG Global High Dividend,Risk Manager"""

        # Parse the CSV data
        reader = csv.DictReader(csv_data.splitlines())

        # Iterate over the rows and create instances
        for row in reader:
            try:
                # Get or create related instances
                entity_instance = PEP_Entities.objects.get_or_create(entity_name=row['Entity Name'])[0]
                name_instance = PEP_Names.objects.get_or_create(pep_name=row['PEP Name'])[0]
                
                # department_instance = Person_Reviewers.objects.get_or_create(name=row['Reviewer Department'])[0]
                # reviewer_instance = Person_Reviewers.objects.get_or_create(lastname=row['Reviewer Name'].split()[0], firstname=row['Reviewer Name'].split()[1],defaults={'slfm_department_compliance_id':9})[0]

                reviewer_instance, created = Person_Reviewers.objects.get_or_create(
                    lastname=row['Reviewer Name'].split()[0],
                    firstname=row['Reviewer Name'].split()[1],
                    defaults={
                        'slfm_department_compliance_id': 9,
                        'person_email': '',  # required if not nullable
                        'slfm_department_name': 'Default Dept',
                        'sub_department_name': 'Default Subdept'
                    }
                )

                # Ensure required fields are set even if the instance already existed
                if not created:
                    updated = False
                    if reviewer_instance.slfm_department_compliance_id is None:
                        reviewer_instance.slfm_department_compliance_id = 9
                        updated = True
                    if not reviewer_instance.person_email:
                        reviewer_instance.person_email = ''
                        updated = True
                    if not reviewer_instance.slfm_department_name:
                        reviewer_instance.slfm_department_name = 'Default Dept'
                        updated = True
                    if not reviewer_instance.sub_department_name:
                        reviewer_instance.sub_department_name = 'Default Subdept'
                        updated = True
                    if updated:
                        reviewer_instance.save()



                rc_validator_instance = Person_Reviewers.objects.get_or_create(lastname=row['RC Validator Name'].split()[0], firstname=row['RC Validator Name'].split()[1])[0]

                slamlux_classification_instance = PEP_Classifications.objects.get_or_create(classification_status=row['Slamlux Classification'])[0]
                ta_classification_instance = PEP_Classifications.objects.get_or_create(classification_status=row['TA Classification'])[0]
                slamlux_estimation_instance = PEP_Estimations.objects.get_or_create(estimation_status=row['Slamlux Estimation'])[0]
                ta_estimation_instance = PEP_Estimations.objects.get_or_create(estimation_status=row['TA Estimation'])[0]
                nationality_instance = PEP_Nationality.objects.get_or_create(nationality=row['Nationality'])[0]
                service_provider_instance = ServiceProviderType.objects.get_or_create(type=row['Service Provider Type'])[0]

                # Create or get the entity-name relationship
                entity_name_instance = PEP_Entities_Names.objects.get_or_create(entities_id_fk=entity_instance,
                                                                                names_id_fk=name_instance,
                                                                                removed=False)[0]

                # Create or get the dates instance
                pep_dates_instance = PEP_Dates.objects.get_or_create(entities_names_id_fk=entity_name_instance,
                                                                     date_added=parse_date(row['Date Added']),
                                                                     date_validation_rc=parse_date(row['Date RC Validation']),
                                                                     date_approval_mc=parse_date(row['Date Approval MC']),
                                                                     date_approval_brd=parse_date(row['Date Approval Board']),
                                                                     date_updated_last=parse_date(row['Date Updated']))[0]

                # Create or get the PEP_Name_Screening instance
                pep_name_screening_instance = PEP_Name_Screening.objects.get_or_create(result_type=row['PEP Name'])[0]

                # Fetch existing Fund and Subfund instances
                try:
                    fund_name = row['Fund Name'].strip()
                    print(f"Searching for Fund with name: '{fund_name}'")
                    fund_instance = Fund.objects.get(fund_name__iexact=fund_name)
                except Exception as e:
                    print(f"Fund with name '{fund_name}' does not exist.: {e}")
                    continue
                try:
                    subfund_name = row['Subfund Name'].strip()
                    print(f"Searching for Subfund with name: '{subfund_name}'")
                    subfund_instance = Subfund.objects.get(subfund_name__iexact=subfund_name, fund_id_fk=fund_instance)
                except Exception as e:
                    print(f"Subfund with name '{subfund_name}' does not exist.: {e}")
                    continue
                
                # Create the PEP_Entities_Subfund instance
                entity_subfund_instance = PEP_Entities_Subfund.objects.get_or_create(entities_id_fk=entity_instance, subfund_id_fk=subfund_instance)[0]

                # Create the PEP_Info instance
                pep_info_instance = PEP_Info.objects.create(
                    entities_names_id_fk=entity_name_instance,
                    pep_names_screening_id_fk=pep_name_screening_instance,
                    comment_screening=row['Comment Screening'],
                    comment_assessment=row['Comment Assessment'],
                    person_reviewers_id_fk=reviewer_instance,
                    rc_validation_id_fk=rc_validator_instance,
                    slamlux_classification_id_fk=slamlux_classification_instance,
                    ta_classification_id_fk=ta_classification_instance,
                    slamlux_estimation_id_fk=slamlux_estimation_instance,
                    ta_estimation_id_fk=ta_estimation_instance,
                    pep_nationality_id_fk=nationality_instance,
                    pep_dates_id_fk=pep_dates_instance,
                    service_provider=service_provider_instance,
                    is_rr_validated=False,
                    comment_mc_board=row['Comment MC Board'],
                    pep_remove_reason=row['PEP Remove Reason']
                )
                print(f"Successfully processed row: {row} \n")
            except Exception as e:
                print(f"Error processing row: {row}. Exception: {e} \n")


    # COI
    def load_coi_status(self):
        # COI_Status
        data = [
            ('Closed'),
            ('Mitigated'),
            ('Ongoing mitigation')
        ]
        status = [COI_Status(status_description = es) for es in data]
        COI_Status.objects.bulk_create(status)

    def add_initial_coi_data(self):
        # Define the CSV data
        csv_data = """COI Info ID,Area of Conflict,Event Description,Reviewer Name,Status Description,Date Added,Date Review MC,Date Review Board,Date Updated,Unit,Mitigation Measures,Fund Name,Subfund Name
        1,Conflict1,Description1,G Miriam,Closed,2025-03-14,2025-03-14,2025-03-14,2025-03-14,Unit1,Measures1,Alpha Growth Fund,Funds (LUX) - Equity ESG Global High Dividend
        2,Conflict2,Description2,Papadopoulou Aikaterini,Closed,2025-03-14,2025-03-14,2025-03-14,2025-03-14,Unit2,Measures2,Alpha Growth Fund,Funds (LUX) - Equity ESG Global High Dividend"""

        # Parse the CSV data
        reader = csv.DictReader(csv_data.splitlines())

        # Iterate over the rows and create instances
        for row in reader:
            try:
                # Get or create related instances
                fund_instance = Fund.objects.get(fund_name=row['Fund Name'])
                subfund_instance = Subfund.objects.get(subfund_name=row['Subfund Name'], fund_id_fk=fund_instance)
                status_instance, _ = COI_Status.objects.get_or_create(status_description=row['Status Description'])

                # Create or get the COI_Cases instance
                coi_case_instance, _ = COI_Cases.objects.get_or_create(area_of_conflict=row['Area of Conflict'], event_description=row['Event Description'])
                coi_case_instance.subfunds.add(subfund_instance)

                # Create or get the COI_Dates instance
                coi_dates_instance, _ = COI_Dates.objects.get_or_create(
                    cases_id_fk=coi_case_instance,
                    date_added=parse_date(row['Date Added']),
                    date_review_mc=parse_date(row['Date Review MC']),
                    date_review_brd=parse_date(row['Date Review Board']),
                    date_updated_last=parse_date(row['Date Updated'])
                )

                # Create the COI_Info instance
                coi_info_instance = COI_Info.objects.create(
                    cases_id_fk=coi_case_instance,
                    isProven=False,
                    unit=row['Unit'],
                    mitigation_measures=row['Mitigation Measures'],
                    isInvestorInformed=False,
                    status_id_fk=status_instance,
                    coi_dates_id_fk=coi_dates_instance
                )
                print(f"Successfully processed row: {row} \n")
            except Exception as e:
                print(f"Error processing row: {row}. Exception: {e} \n")

        # Verify the data
        for coi_info in COI_Info.objects.all():
            print(f"COI Info ID: {coi_info.coi_info_id}")
            print(f"Area of Conflict: {coi_info.cases_id_fk.area_of_conflict}")
            print(f"Event Description: {coi_info.cases_id_fk.event_description}")
            print(f"Status Description: {coi_info.status_id_fk.status_description}")
            print(f"Date Added: {coi_info.coi_dates_id_fk.date_added}")
            print(f"Date Review MC: {coi_info.coi_dates_id_fk.date_review_mc}")
            print(f"Date Review Board: {coi_info.coi_dates_id_fk.date_review_brd}")
            print(f"Date Updated: {coi_info.coi_dates_id_fk.date_updated_last}")
            print(f"Unit: {coi_info.unit}")
            print(f"Mitigation Measures: {coi_info.mitigation_measures}")
            print("-----")

    def handle(self, *args, **kwargs):
        self.load_fund_data()
        self.load_subfund_data()
        self.load_service_provider_data
        self.load_person_reviewers_data()
        self.load_pep_estimations_data()
        self.load_pep_classifications_data()
        self.load_pep_names_data()
        self.load_pep_name_screening_data()
        self.load_pep_nationality_data()
        self.add_initial_pep_data()
        self.load_coi_status()
        self.add_initial_coi_data()
        self.stdout.write(self.style.SUCCESS('Successfully loaded data into the database'))