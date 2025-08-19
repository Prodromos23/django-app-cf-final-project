from django import forms
from pep.models import PEP_Names, PEP_Entities,Subfund,PEP_Entities_Subfund,Person_Reviewers,PEP_Info,PEP_Nationality,PEP_Classifications,PEP_Estimations,PEP_Dates,ServiceProviderType,PEP_Entities_Names,PEP_Name_Screening

class PEPNameForm(forms.ModelForm):
    entities_id_fk = forms.ModelChoiceField(queryset=PEP_Entities.objects.all(), label="PEP Entity",required=False)

    class Meta:
        model = PEP_Names
        fields = ['pep_name', 'position', 'entities_id_fk']


class PEPInfoPageForm(forms.ModelForm):
    entity_name = forms.CharField(max_length=255, label="Entity Name")
    subfunds = forms.ModelMultipleChoiceField(
        queryset=Subfund.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label="Subfunds"
    )
    pep_name = forms.CharField(max_length=255, required=False, label="PEP Name")
    position = forms.CharField(max_length=100, required=False, label="Position")
    result_type = forms.CharField(max_length=50, label="Result Type")
    comment_screening = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="Comment Screening")
    comment_assessment = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="Comment Assessment")
    slamlux_classification_id_fk = forms.ModelChoiceField(queryset=PEP_Classifications.objects.all(), label="SLAMLUX Classification")
    ta_classification_id_fk = forms.ModelChoiceField(queryset=PEP_Classifications.objects.all(), label="TA Classification")
    slamlux_estimation_id_fk = forms.ModelChoiceField(queryset=PEP_Estimations.objects.all(), label="SLAMLUX Estimation")
    ta_estimation_id_fk = forms.ModelChoiceField(queryset=PEP_Estimations.objects.all(), label="TA Estimation")
    pep_nationality_id_fk = forms.ModelChoiceField(queryset=PEP_Nationality.objects.all(), label="Nationality")
    service_provider = forms.ModelChoiceField(queryset=ServiceProviderType.objects.all(), label="Service Provider Type")
    removed = forms.BooleanField(required=False, label="Removed")
    date_validation_rc = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Validation RC")
    date_approval_mc = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Approval MC")
    date_approval_brd = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Approval BRD")
    is_rr_validated = forms.BooleanField(required=False, label="Is RR Validated")
    comment_mc_board = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="Comment MC Board")
    pep_remove_reason = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="PEP Remove Reason")
    person_reviewers_id_fk = forms.ModelChoiceField(queryset=Person_Reviewers.objects.all(), label="Person Reviewer")
    rc_validation_id_fk = forms.ModelChoiceField(queryset=Person_Reviewers.objects.all(), label="RC Validation Reviewer")

    class Meta:
        model = PEP_Info
        exclude = ['pep_dates_id_fk', 'entities_names_id_fk', 'pep_names_screening_id_fk', 'slfm_department_name', 'sub_department_name', 'person_email']  # Exclude the specified fields
        fields = [
            'entity_name',
            'subfunds',
            'pep_name',
            'position',
            'result_type',
            'comment_screening',
            'comment_assessment',
            'slamlux_classification_id_fk',
            'ta_classification_id_fk',
            'slamlux_estimation_id_fk',
            'ta_estimation_id_fk',
            'pep_nationality_id_fk',
            'service_provider',
            'removed',
            'date_validation_rc',
            'date_approval_mc',
            'date_approval_brd',
            'is_rr_validated',
            'comment_mc_board',
            'pep_remove_reason',
            'person_reviewers_id_fk',
            'rc_validation_id_fk'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'entities_names_id_fk'):
                self.fields['entity_name'].initial = self.instance.entities_names_id_fk.entities_id_fk.entity_name
                self.fields['subfunds'].initial = self.instance.entities_names_id_fk.entities_id_fk.subfunds.all()
                self.fields['pep_name'].initial = self.instance.entities_names_id_fk.names_id_fk.pep_name
                self.fields['position'].initial = self.instance.entities_names_id_fk.names_id_fk.position
                self.fields['removed'].initial = self.instance.entities_names_id_fk.removed
            if hasattr(self.instance, 'pep_names_screening_id_fk'):
                self.fields['result_type'].initial = self.instance.pep_names_screening_id_fk.result_type
            if hasattr(self.instance, 'pep_dates_id_fk'):
                self.fields['date_validation_rc'].initial = self.instance.pep_dates_id_fk.date_validation_rc
                self.fields['date_approval_mc'].initial = self.instance.pep_dates_id_fk.date_approval_mc
                self.fields['date_approval_brd'].initial = self.instance.pep_dates_id_fk.date_approval_brd
            self.fields['comment_screening'].initial = self.instance.comment_screening
            self.fields['comment_assessment'].initial = self.instance.comment_assessment
            self.fields['slamlux_classification_id_fk'].initial = self.instance.slamlux_classification_id_fk
            self.fields['ta_classification_id_fk'].initial = self.instance.ta_classification_id_fk
            self.fields['slamlux_estimation_id_fk'].initial = self.instance.slamlux_estimation_id_fk
            self.fields['ta_estimation_id_fk'].initial = self.instance.ta_estimation_id_fk
            self.fields['pep_nationality_id_fk'].initial = self.instance.pep_nationality_id_fk
            self.fields['service_provider'].initial = self.instance.service_provider
            self.fields['is_rr_validated'].initial = self.instance.is_rr_validated
            self.fields['comment_mc_board'].initial = self.instance.comment_mc_board
            self.fields['pep_remove_reason'].initial = self.instance.pep_remove_reason
            self.fields['person_reviewers_id_fk'].initial = self.instance.person_reviewers_id_fk
            self.fields['rc_validation_id_fk'].initial = self.instance.rc_validation_id_fk

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Form data is not valid")
        try:
            instance = super().save(commit=False)

            # Create or get related instances
            pep_entity, created = PEP_Entities.objects.get_or_create(entity_name=self.cleaned_data['entity_name'])
            pep_entity.subfunds.set(self.cleaned_data['subfunds'])

            pep_name = PEP_Names.objects.filter(
                pep_name=self.cleaned_data['pep_name'],
                position=self.cleaned_data['position']
            ).first()
            if not pep_name:
                pep_name = PEP_Names.objects.create(
                    pep_name=self.cleaned_data['pep_name'],
                    position=self.cleaned_data['position']
                )

            pep_entities_names, created = PEP_Entities_Names.objects.get_or_create(
                entities_id_fk=pep_entity,
                names_id_fk=pep_name,
                removed=self.cleaned_data['removed']
            )
            # Assign the new PEP_Entities_Names instance to PEP_Info
            instance.entities_names_id_fk = pep_entities_names

            pep_name_screening = PEP_Name_Screening.objects.filter(result_type=self.cleaned_data['result_type']).first()
            if not pep_name_screening:
                pep_name_screening = PEP_Name_Screening.objects.create(result_type=self.cleaned_data['result_type'])
            instance.pep_names_screening_id_fk = pep_name_screening  # Assign the screening instance

            pep_dates = PEP_Dates.objects.create(
                entities_names_id_fk=pep_entities_names,
                date_validation_rc=self.cleaned_data['date_validation_rc'],
                date_approval_mc=self.cleaned_data['date_approval_mc'],
                date_approval_brd=self.cleaned_data['date_approval_brd'],
                date_removal=None,  # Automatically set later
                date_updated_last=None  # Automatically set later
            )

            instance.pep_dates_id_fk = pep_dates  # Assign the dates instance

            if commit:
                instance.save()

            # Automatically populate date_removal and date_updated_last
            pep_dates.date_removal = self.cleaned_data.get('date_removal', None)
            pep_dates.date_updated_last = self.cleaned_data.get('date_updated_last', None)

            pep_dates.save()

            return instance
        except Exception as e:
            raise ValueError(f"Error saving PEP_Info form: {e}")

class PEPInfoAdminForm(forms.ModelForm):
    entities_names_id_fk = forms.ModelChoiceField(queryset=PEP_Entities_Names.objects.all(), label="Entity Name")
    subfunds = forms.ModelMultipleChoiceField(
        queryset=Subfund.objects.all(),
        # widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        widget=forms.HiddenInput(),
        required=False,
        label="Subfunds"
    )
    result_type = forms.CharField(max_length=50, label="Result Type")
    comment_screening = forms.CharField(widget=forms.Textarea, required=False, label="Comment Screening")
    comment_assessment = forms.CharField(widget=forms.Textarea, required=False, label="Comment Assessment")
    slamlux_classification_id_fk = forms.ModelChoiceField(queryset=PEP_Classifications.objects.all(), label="SLAMLUX Classification")
    ta_classification_id_fk = forms.ModelChoiceField(queryset=PEP_Classifications.objects.all(), label="TA Classification")
    slamlux_estimation_id_fk = forms.ModelChoiceField(queryset=PEP_Estimations.objects.all(), label="SLAMLUX Estimation")
    ta_estimation_id_fk = forms.ModelChoiceField(queryset=PEP_Estimations.objects.all(), label="TA Estimation")
    pep_nationality_id_fk = forms.ModelChoiceField(queryset=PEP_Nationality.objects.all(), label="Nationality")
    service_provider = forms.ModelChoiceField(queryset=ServiceProviderType.objects.all(), label="Service Provider Type")
    removed = forms.BooleanField(required=False, label="Removed")
    date_validation_rc = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Validation RC")
    date_approval_mc = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Approval MC")
    date_approval_brd = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Approval BRD")
    is_rr_validated = forms.BooleanField(required=False, label="Is RR Validated")
    comment_mc_board = forms.CharField(widget=forms.Textarea, required=False, label="Comment MC Board")
    pep_remove_reason = forms.CharField(widget=forms.Textarea, required=False, label="PEP Remove Reason")
    person_reviewers_id_fk = forms.ModelChoiceField(queryset=Person_Reviewers.objects.all(), label="Person Reviewer")
    rc_validation_id_fk = forms.ModelChoiceField(queryset=Person_Reviewers.objects.all(), label="RC Validation Reviewer")

    class Meta:
        model = PEP_Info
        exclude = ['pep_dates_id_fk', 'pep_names_screening_id_fk', 'slfm_department_name', 'sub_department_name', 'person_email']
        fields = [
            'entities_names_id_fk',
            'subfunds',
            'result_type',
            'comment_screening',
            'comment_assessment',
            'slamlux_classification_id_fk',
            'ta_classification_id_fk',
            'slamlux_estimation_id_fk',
            'ta_estimation_id_fk',
            'pep_nationality_id_fk',
            'service_provider',
            'removed',
            'date_validation_rc',
            'date_approval_mc',
            'date_approval_brd',
            'is_rr_validated',
            'comment_mc_board',
            'pep_remove_reason',
            'person_reviewers_id_fk',
            'rc_validation_id_fk'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'entities_names_id_fk'):
                self.fields['entities_names_id_fk'].initial = self.instance.entities_names_id_fk
                self.fields['subfunds'].initial = self.instance.entities_names_id_fk.entities_id_fk.subfunds.all()
                self.fields['removed'].initial = self.instance.entities_names_id_fk.removed
            if hasattr(self.instance, 'pep_names_screening_id_fk'):
                self.fields['result_type'].initial = self.instance.pep_names_screening_id_fk.result_type
            if hasattr(self.instance, 'pep_dates_id_fk'):
                self.fields['date_validation_rc'].initial = self.instance.pep_dates_id_fk.date_validation_rc
                self.fields['date_approval_mc'].initial = self.instance.pep_dates_id_fk.date_approval_mc
                self.fields['date_approval_brd'].initial = self.instance.pep_dates_id_fk.date_approval_brd
            self.fields['comment_screening'].initial = self.instance.comment_screening
            self.fields['comment_assessment'].initial = self.instance.comment_assessment
            self.fields['slamlux_classification_id_fk'].initial = self.instance.slamlux_classification_id_fk
            self.fields['ta_classification_id_fk'].initial = self.instance.ta_classification_id_fk
            self.fields['slamlux_estimation_id_fk'].initial = self.instance.slamlux_estimation_id_fk
            self.fields['ta_estimation_id_fk'].initial = self.instance.ta_estimation_id_fk
            self.fields['pep_nationality_id_fk'].initial = self.instance.pep_nationality_id_fk
            self.fields['service_provider'].initial = self.instance.service_provider
            self.fields['is_rr_validated'].initial = self.instance.is_rr_validated
            self.fields['comment_mc_board'].initial = self.instance.comment_mc_board
            self.fields['pep_remove_reason'].initial = self.instance.pep_remove_reason
            self.fields['person_reviewers_id_fk'].initial = self.instance.person_reviewers_id_fk
            self.fields['rc_validation_id_fk'].initial = self.instance.rc_validation_id_fk

    # def save(self, commit=True):
    #     if not self.is_valid():
    #         raise ValueError("Form data is not valid")
        
    #     try:
    #         instance = super().save(commit=False)
    #         # # Automatically assign coi_dates_id_fk based on selected case
    #         # if not instance.pep_dates_id_fk_id:
    #         #     try:
    #         #         instance.pep_dates_id_fk_id = PEP_Dates.objects.get(entities_names_id_fk=instance.entities_names_id_fk)
    #         #     except PEP_Dates.DoesNotExist:
    #         #         raise ValueError("No PEP_Dates entry found for the selected case.")
    #         # Update related instances
    #         pep_entity = instance.entities_names_id_fk.entities_id_fk
    #         # pep_entity.entity_name = self.cleaned_data['entity_name']
    #         pep_entity.save()
    #         pep_entity.subfunds.set(self.cleaned_data['subfunds'])
    #         pep_entities_names = instance.entities_names_id_fk
    #         pep_entities_names.removed = self.cleaned_data['removed']
    #         pep_entities_names.save()
    #         pep_name_screening = instance.pep_names_screening_id_fk
    #         # pep_name_screening = instance.pep_names_screening_id_fk_id
    #         pep_name_screening.result_type = self.cleaned_data['result_type']
    #         pep_name_screening.save()
            
    #         # PEP Dates
    #         pep_dates = instance.pep_dates_id_fk
    #         pep_dates.date_validation_rc = self.cleaned_data['date_validation_rc']
    #         pep_dates.date_approval_mc = self.cleaned_data['date_approval_mc']
    #         pep_dates.date_approval_brd = self.cleaned_data['date_approval_brd']
    #         pep_dates.date_removal = self.cleaned_data.get('date_removal', None)
    #         pep_dates.date_updated_last = self.cleaned_data.get('date_updated_last', None)
    #         pep_dates.save()


    #         # Update PEP_Info instance
    #         instance.comment_screening = self.cleaned_data['comment_screening']
    #         instance.comment_assessment = self.cleaned_data['comment_assessment']
    #         instance.person_reviewers_id_fk = self.cleaned_data['person_reviewers_id_fk']
    #         instance.rc_validation_id_fk = self.cleaned_data['rc_validation_id_fk']
    #         instance.slamlux_classification_id_fk = self.cleaned_data['slamlux_classification_id_fk']
    #         instance.ta_classification_id_fk = self.cleaned_data['ta_classification_id_fk']
    #         instance.slamlux_estimation_id_fk = self.cleaned_data['slamlux_estimation_id_fk']
    #         instance.ta_estimation_id_fk = self.cleaned_data['ta_estimation_id_fk']
    #         instance.pep_nationality_id_fk = self.cleaned_data['pep_nationality_id_fk']
    #         instance.service_provider = self.cleaned_data['service_provider']
    #         instance.is_rr_validated = self.cleaned_data['is_rr_validated']
    #         instance.comment_mc_board = self.cleaned_data['comment_mc_board']
    #         instance.pep_remove_reason = self.cleaned_data['pep_remove_reason']
    #         if commit:
    #             instance.save()

    #         # pep_dates.date_removal = instance.date_removal
    #         # pep_dates.date_updated_last = instance.date_updated_last

    #         return instance
    #     except Exception as e:
    #         raise ValueError(f"Error saving PEP_Info form: {e}")


    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Form data is not valid")

        try:
            instance = super().save(commit=False)

            # Assign or create PEP_Dates FIRST
            pep_dates, _ = PEP_Dates.objects.get_or_create(
                entities_names_id_fk=instance.entities_names_id_fk
            )
            pep_dates.date_validation_rc = self.cleaned_data.get('date_validation_rc')
            pep_dates.date_approval_mc = self.cleaned_data.get('date_approval_mc')
            pep_dates.date_approval_brd = self.cleaned_data.get('date_approval_brd')
            pep_dates.date_removal = self.cleaned_data.get('date_removal')
            pep_dates.date_updated_last = self.cleaned_data.get('date_updated_last')
            pep_dates.save()

            # Assign the FK before saving the instance
            instance.pep_dates_id_fk = pep_dates

            # Create or get screening result
            result_type = self.cleaned_data.get('result_type')
            screening, _ = PEP_Name_Screening.objects.get_or_create(result_type=result_type)
            instance.pep_names_screening_id_fk = screening

            # Set other fields
            instance.comment_screening = self.cleaned_data['comment_screening']
            instance.comment_assessment = self.cleaned_data['comment_assessment']
            instance.person_reviewers_id_fk = self.cleaned_data['person_reviewers_id_fk']
            instance.rc_validation_id_fk = self.cleaned_data['rc_validation_id_fk']
            instance.slamlux_classification_id_fk = self.cleaned_data['slamlux_classification_id_fk']
            instance.ta_classification_id_fk = self.cleaned_data['ta_classification_id_fk']
            instance.slamlux_estimation_id_fk = self.cleaned_data['slamlux_estimation_id_fk']
            instance.ta_estimation_id_fk = self.cleaned_data['ta_estimation_id_fk']
            instance.pep_nationality_id_fk = self.cleaned_data['pep_nationality_id_fk']
            instance.service_provider = self.cleaned_data['service_provider']
            instance.is_rr_validated = self.cleaned_data['is_rr_validated']
            instance.comment_mc_board = self.cleaned_data['comment_mc_board']
            instance.pep_remove_reason = self.cleaned_data['pep_remove_reason']

            if commit:
                instance.save()

                # Update subfunds
                subfunds = self.cleaned_data.get('subfunds')
                if subfunds:
                    entity = instance.entities_names_id_fk.entities_id_fk
                    PEP_Entities_Subfund.objects.filter(entities_id_fk=entity).delete()
                    for subfund in subfunds:
                        PEP_Entities_Subfund.objects.create(entities_id_fk=entity, subfund_id_fk=subfund)

            return instance

        except Exception as e:
            raise ValueError(f"Error saving PEP_Info form: {e}")


# def save(self, commit=True):
#     if not self.is_valid():
#         raise ValueError("Form data is not valid")

#     try:
#         instance = super().save(commit=False)

#         # Assign or create PEP_Dates
#         pep_dates, _ = PEP_Dates.objects.get_or_create(entities_names_id_fk=instance.entities_names_id_fk)
#         pep_dates.date_validation_rc = self.cleaned_data.get('date_validation_rc')
#         pep_dates.date_approval_mc = self.cleaned_data.get('date_approval_mc')
#         pep_dates.date_approval_brd = self.cleaned_data.get('date_approval_brd')
#         pep_dates.date_removal = self.cleaned_data.get('date_removal')
#         pep_dates.date_updated_last = self.cleaned_data.get('date_updated_last')
#         pep_dates.save()
#         instance.pep_dates_id_fk = pep_dates

#         # Assign or create PEP_Name_Screening
#         result_type = self.cleaned_data.get('result_type')
#         screening, _ = PEP_Name_Screening.objects.get_or_create(result_type=result_type)
#         instance.pep_names_screening_id_fk = screening

#         # Update related instances
#         pep_entity = instance.entities_names_id_fk.entities_id_fk
#         pep_entity.subfunds.set(self.cleaned_data['subfunds'])
#         pep_entity.save()

#         pep_entities_names = instance.entities_names_id_fk
#         pep_entities_names.removed = self.cleaned_data['removed']
#         pep_entities_names.save()

#         # Update PEP_Info fields
#         instance.comment_screening = self.cleaned_data['comment_screening']
#         instance.comment_assessment = self.cleaned_data['comment_assessment']
#         instance.person_reviewers_id_fk = self.cleaned_data['person_reviewers_id_fk']
#         instance.rc_validation_id_fk = self.cleaned_data['rc_validation_id_fk']
#         instance.slamlux_classification_id_fk = self.cleaned_data['slamlux_classification_id_fk']
#         instance.ta_classification_id_fk = self.cleaned_data['ta_classification_id_fk']
#         instance.slamlux_estimation_id_fk = self.cleaned_data['slamlux_estimation_id_fk']
#         instance.ta_estimation_id_fk = self.cleaned_data['ta_estimation_id_fk']
#         instance.pep_nationality_id_fk = self.cleaned_data['pep_nationality_id_fk']
#         instance.service_provider = self.cleaned_data['service_provider']
#         instance.is_rr_validated = self.cleaned_data['is_rr_validated']
#         instance.comment_mc_board = self.cleaned_data['comment_mc_board']
#         instance.pep_remove_reason = self.cleaned_data['pep_remove_reason']

#         if commit:
#             instance.save()

#         return instance

#     except Exception as e:
#         raise ValueError(f"Error saving PEP_Info form: {e}")



