from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from .forms import UserRegistrationForm
from pep.models import Person_Reviewers
from conflict_of_interests.forms import COIInfoPageForm,COIInfoAdminForm
from pep.forms import PEPInfoAdminForm,PEPInfoPageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.management import call_command
from pep.models import PEP_Info
from conflict_of_interests.models import COI_Info
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models.functions import Lower


def register(request):
    '''
    Registration and assignment of Groups to the new registers. If email of new registration exist in the list of Person_Reviewers emails then the Group1 is assigned otherwise Group2 is assigned.
    '''
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True  # Ensure the user is active
            user.is_staff = True  # Set the user as staff
            user.save()

            # Check if the email exists in Person_Reviewers
            email = form.cleaned_data['email']
            # if Person_Reviewers.objects.filter(person_email=email).exists() or Person_Reviewers.objects.filter(person_email=email.lower()).exists():
            # if Person_Reviewers.objects.annotate(email_lower=Lower('person_email')).filter(email_lower=email).exists():
            if Person_Reviewers.objects.filter(person_email__iexact=email).exists():
                group_name = 'Group1'
            else:
                group_name = 'Group2'

            # Assign the user to the appropriate group
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, f'{group_name} does not exist.')

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('/admin/login/?next=/admin/')  # Redirect to the admin login page
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

# For Admin
def edit_pep_info(request, pep_info_id):
    pep_info_instance = get_object_or_404(PEP_Info, pk=pep_info_id)
    if request.method == 'POST':
        form = PEPInfoAdminForm(request.POST, instance=pep_info_instance)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = PEPInfoAdminForm(instance=pep_info_instance)
    return render(request, 'edit_pep_info/edit_pep_info.html', {'form': form})

# For Admin
def edit_coi_info(request, coi_info_id):
    coi_info_instance = get_object_or_404(COI_Info, pk=coi_info_id)
    if request.method == 'POST':
        form = COIInfoAdminForm(request.POST, instance=coi_info_instance)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = COIInfoAdminForm(instance=coi_info_instance)
    return render(request, 'edit_pep_info/edit_pep_info.html', {'form': form})

# coi UPDATE form
def coi_info_update_view(request, pk):
    instance = get_object_or_404(PEP_Info, pk=pk)
    if request.method == 'POST':
        form = COIInfoPageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = COIInfoPageForm(instance=instance)
    return render(request, 'create_coi_info/create_coi_info.html', {'form': form})

# COI Info Page form
def coi_info_create_page(request):
    if request.method == 'POST':
        form = COIInfoPageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = COIInfoPageForm()
    return render(request, 'create_coi_info/create_coi_info.html', {'form': form})

# PEP Info Page form
def pep_info_create_page(request):
    if request.method == 'POST':
        form = PEPInfoPageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = PEPInfoPageForm()
    return render(request, 'create_pep_info/create_pep_info.html', {'form': form})
# PEP UPDATE form
def pep_info_update_view(request, pk):
    instance = get_object_or_404(PEP_Info, pk=pk)
    if request.method == 'POST':
        form = PEPInfoPageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = PEPInfoPageForm(instance=instance)
    return render(request, 'create_pep_info/create_pep_info.html', {'form': form})


# Access the welcome page after login 
class custom_login_view(LoginView):
    template_name = 'admin/login.html'
    success_url = reverse_lazy('welcome')  # Redirect to the welcome page

    def get_success_url(self):
        return self.success_url

# Success
def success_view(request):
    return render(request, 'success.html')  # Render a success template

# Shutdown
def shutdown_view(request):
    if request.method == 'POST':
        call_command('shutdown_server')
        return JsonResponse({'status': 'Server shutting down...'})
    return render(request, 'shutdown.html')


# ____________________________________
