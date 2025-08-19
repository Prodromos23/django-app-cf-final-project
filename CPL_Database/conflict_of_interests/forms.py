from django import forms
from .models import COI_Info,COI_Dates
from .models import COI_Status, COI_Cases, COI_Cases_Subfund, COI_Dates, COI_Info
from pep.models import Subfund

class COIInfoPageForm(forms.ModelForm):
    area_of_conflict = forms.CharField(max_length=150, label="Area of Conflict")
    status_description = forms.CharField(max_length=255, label="Status Description")
    event_description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="Event Description")
    removed = forms.BooleanField(required=False, label="Removed")
    subfunds = forms.ModelMultipleChoiceField(
        queryset=Subfund.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label="Subfunds"
    )
    date_review_mc = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Review MC")
    date_review_brd = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Review BRD")
    isProven = forms.BooleanField(required=False, label="Is Proven")
    unit = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="Unit")
    mitigation_measures = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=False, label="Mitigation Measures")
    isInvestorInformed = forms.BooleanField(required=False, label="Is Investor Informed")
    status_id_fk = forms.ModelChoiceField(queryset=COI_Status.objects.all(), label="Status")
    coi_dates_id_fk = forms.ModelChoiceField(queryset=COI_Dates.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = COI_Info
        fields = [
            'area_of_conflict', 'status_description', 'event_description', 'removed', 'subfunds',
            'date_review_mc', 'date_review_brd',
            'isProven', 'unit', 'mitigation_measures', 'isInvestorInformed', 'status_id_fk', 'coi_dates_id_fk'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coi_dates_id_fk'].label = ""
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'cases_id_fk'):
                self.fields['area_of_conflict'].initial = self.instance.cases_id_fk.area_of_conflict
                self.fields['event_description'].initial = self.instance.cases_id_fk.event_description
            if hasattr(self.instance, 'status_id_fk'):
                self.fields['status_description'].initial = self.instance.status_id_fk.status_description
            if hasattr(self.instance, 'coi_dates_id_fk'):
                self.fields['date_review_mc'].initial = self.instance.coi_dates_id_fk.date_review_mc
                self.fields['date_review_brd'].initial = self.instance.coi_dates_id_fk.date_review_brd
            self.fields['isProven'].initial = self.instance.isProven
            self.fields['unit'].initial = self.instance.unit
            self.fields['mitigation_measures'].initial = self.instance.mitigation_measures
            self.fields['isInvestorInformed'].initial = self.instance.isInvestorInformed
            self.fields['removed'].initial = self.instance.cases_id_fk.removed if hasattr(self.instance.cases_id_fk, 'removed') else None
            self.fields['subfunds'].initial = self.instance.cases_id_fk.subfunds.all() if hasattr(self.instance.cases_id_fk, 'subfunds') else None

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Create related instances
        coi_status = COI_Status.objects.create(status_description=self.cleaned_data['status_description'])
        coi_case = COI_Cases.objects.create(
            area_of_conflict=self.cleaned_data['area_of_conflict'],
            event_description=self.cleaned_data['event_description'],
            removed=self.cleaned_data['removed']
        )
        coi_case.subfunds.set(self.cleaned_data['subfunds'])

        coi_dates = COI_Dates.objects.create(
            cases_id_fk=coi_case,
            date_review_mc=self.cleaned_data['date_review_mc'],
            date_review_brd=self.cleaned_data['date_review_brd'],
            date_removal=None,  # Automatically set later
            date_updated_last=None  # Automatically set later
        )
        
        # Assign the newly created instances to the COI_Info instance
        instance.cases_id_fk = coi_case
        instance.status_id_fk = coi_status
        instance.coi_dates_id_fk = coi_dates
        
        if commit:
            instance.save()
        
        # Automatically populate date_removal and date_updated_last
        coi_dates.date_removal = self.cleaned_data.get('date_removal', None)
        coi_dates.date_updated_last = self.cleaned_data.get('date_updated_last', None)
        coi_dates.save()
        
        return instance


class COIInfoAdminForm(forms.ModelForm):
    cases_id_fk = forms.ModelChoiceField(queryset=COI_Cases.objects.all(), label="Case")
    subfunds = forms.ModelMultipleChoiceField(
        queryset=Subfund.objects.all(),
        # widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        widget=forms.HiddenInput(),
        required=False,
        label="Subfunds"
    )
    status_description = forms.CharField(max_length=255, label="Status Description")
    event_description = forms.CharField(widget=forms.Textarea, required=False, label="Event Description")
    removed = forms.BooleanField(required=False, label="Removed")
    date_review_mc = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Review MC")
    date_review_brd = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Review BRD")
    isProven = forms.BooleanField(required=False, label="Is Proven")
    unit = forms.CharField(widget=forms.Textarea, required=False, label="Unit")
    mitigation_measures = forms.CharField(widget=forms.Textarea, required=False, label="Mitigation Measures")
    isInvestorInformed = forms.BooleanField(required=False, label="Is Investor Informed")
    status_id_fk = forms.ModelChoiceField(queryset=COI_Status.objects.all(), label="Status")
    # coi_dates_id_fk = forms.ModelChoiceField(queryset=COI_Dates.objects.all(), widget=forms.HiddenInput())
    coi_dates_id_fk = forms.ModelChoiceField(queryset=COI_Dates.objects.all(),label="Dates----")
    
    class Meta:
        model = COI_Info
        # exclude = ['coi_dates_id_fk']
        fields = [
            'cases_id_fk',
            # 'subfunds',
            'status_description',
            'event_description',
            'removed',
            'date_review_mc',
            'date_review_brd',
            'isProven',
            'unit',
            'mitigation_measures',
            'isInvestorInformed',
            'status_id_fk',
            # 'coi_dates_id_fk'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'cases_id_fk'):
                self.fields['cases_id_fk'].initial = self.instance.cases_id_fk
                self.fields['subfunds'].initial = self.instance.cases_id_fk.subfunds.all()
                self.fields['removed'].initial = self.instance.cases_id_fk.removed
            if hasattr(self.instance, 'status_id_fk'):
                self.fields['status_description'].initial = self.instance.status_id_fk.status_description
            if hasattr(self.instance, 'coi_dates_id_fk'):
                self.fields['date_review_mc'].initial = self.instance.coi_dates_id_fk.date_review_mc
                self.fields['date_review_brd'].initial = self.instance.coi_dates_id_fk.date_review_brd
            self.fields['event_description'].initial = self.instance.cases_id_fk.event_description
            self.fields['isProven'].initial = self.instance.isProven
            self.fields['unit'].initial = self.instance.unit
            self.fields['mitigation_measures'].initial = self.instance.mitigation_measures
            self.fields['isInvestorInformed'].initial = self.instance.isInvestorInformed

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Form data is not valid")
        try:
            instance = super().save(commit=False)
            # Update related instances

            # Automatically assign coi_dates_id_fk based on selected case
            if not instance.coi_dates_id_fk:
                try:
                    instance.coi_dates_id_fk = COI_Dates.objects.get(cases_id_fk=instance.cases_id_fk)
                except COI_Dates.DoesNotExist:
                    raise ValueError("No COI_Dates entry found for the selected case.")

            coi_case = instance.cases_id_fk
            # coi_case.area_of_conflict = self.cleaned_data['area_of_conflict']
            coi_case.event_description = self.cleaned_data['event_description']
            coi_case.removed = self.cleaned_data['removed']
            coi_case.save()
            coi_case.subfunds.set(self.cleaned_data['subfunds'])
            coi_status = instance.status_id_fk
            coi_status.status_description = self.cleaned_data['status_description']
            coi_status.save()
            coi_dates = instance.coi_dates_id_fk
            coi_dates.date_review_mc = self.cleaned_data['date_review_mc']
            coi_dates.date_review_brd = self.cleaned_data['date_review_brd']
            coi_dates.date_removal = self.cleaned_data.get('date_removal', None)
            coi_dates.date_updated_last = self.cleaned_data.get('date_updated_last', None)
            coi_dates.save()
            # Update COI_Info instance
            instance.isProven = self.cleaned_data['isProven']
            instance.unit = self.cleaned_data['unit']
            instance.mitigation_measures = self.cleaned_data['mitigation_measures']
            instance.isInvestorInformed = self.cleaned_data['isInvestorInformed']
            if commit:
                instance.save()
            return instance
        except Exception as e:
            raise ValueError(f"Error saving COI_Info form: {e}")
    




