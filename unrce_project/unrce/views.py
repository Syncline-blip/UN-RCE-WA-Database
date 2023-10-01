from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import RegistrationForm, InterestForm
from .models import Report, Account, ReportImages, Expression_of_interest, ReportFiles,themes_esd, priority_action_areas, AUDIENCE_CHOICES, DELIVERY_CHOICES, FREQUENCY_CHOICES
from django.http import HttpResponseServerError, JsonResponse  
from django.core.files.storage import FileSystemStorage
import os, json
import pandas as pd
from django.contrib import messages
import logging
from django.db.models import Q
from .forms import (BasicInfoForm, FocalPointsAffiliationsForm, 
                    GeographicalEducationInfoForm, ContentInfoForm, 
                    SustainableDevelopmentGoalsForm, ReportImagesForm, 
                    ReportFilesForm, OrganizationForm, OrganizationInlineFormSet)

logger = logging.getLogger(__name__)
from django.shortcuts import render
# sample data, not to be used, just for testing
project = [
    {
        'author': 'JOHN JOHN',
        'project': 'PROJECT LIVE',
        'project_code': 22341
    }
]
def home(request):
    return render(request, 'unrce/initial-landing.html')


@login_required
def create_report(request, step):
    steps = ['basic', 'focal', 'geoedu', 'content', 'sdg', 'images', 'files', 'org', 'finish']
    try:
        current_index = steps.index(step)
    except ValueError:
        messages.error(request, "Invalid step.")
        return redirect('home')  # Change to actual view

    previous_step = steps[current_index - 1] if current_index > 0 else None

    session_data = request.session.get('form_data', {})

    form_class = get_step_form(step)
    if form_class is None:
        messages.error(request, "Invalid step.")
        return redirect('home')  # Change to actual view

    form = form_class(request.POST or None, initial=session_data.get(step, {}), prefix=step)

    if step == 'focal':
        organizations_formset = OrganizationInlineFormSet(request.POST or None, prefix='organizations')
    else:
        organizations_formset = None

    if request.method == 'POST':
        if form.is_valid() and (organizations_formset is None or organizations_formset.is_valid()):
            cleaned_data = form.cleaned_data
            if 'linked_users' in cleaned_data:
                cleaned_data['linked_users'] = [model_to_dict(user) for user in cleaned_data['linked_users']]
            session_data[step] = cleaned_data
            if organizations_formset is not None:
                orgs_data = [form.cleaned_data for form in organizations_formset if form.is_valid()]
                session_data['organizations'] = orgs_data
                    
            print("Cleaned data:")
            print(cleaned_data)
        
            try:
                request.session['form_data'] = session_data
            except TypeError as e:
                print("Error:", e)
                print("Data causing the error:")
                print(session_data)
                return HttpResponse("An error occurred. Check the console for details.")

            next_step = get_next_step(step)
            if next_step:
                return redirect('create_report_step', step=next_step)
            else:
                messages.error(request, "You have reached the final step.")
        else:
            messages.error(request, "There are errors in the form.")


    context = {
        'form': form,
        'organizations_formset': organizations_formset if step == 'focal' else None,
        'previous_step': previous_step,
        'step': step
    }

    return render(request, 'create_report.html', context)




def get_step_form(step, *args, **kwargs):
    """Return the appropriate form for the given step"""
    forms = {
        'basic': BasicInfoForm,
        'focal': FocalPointsAffiliationsForm,
        'geoedu': GeographicalEducationInfoForm,
        'content': ContentInfoForm,
        'sdg': SustainableDevelopmentGoalsForm,
        'images': ReportImagesForm,
        'files': ReportFilesForm,
        'org': OrganizationForm,
        'finish': None  # We'll handle the 'finish' step differently
    }
    return forms.get(step, None)

def get_next_step(current_step):
    """Return the next step after the given step"""
    steps = ['basic', 'focal', 'geoedu', 'content', 'sdg', 'images', 'files', 'org', 'finish']
    try:
        current_index = steps.index(current_step)
        return steps[current_index + 1] if current_index + 1 < len(steps) else None
    except ValueError:
        messages.error(request, "Invalid step.")
        return None 


@login_required
def finish_report(request):
    session_data = request.session.get('form_data', {})
    if session_data:
        combined_data = {}
        for data in session_data.values():
            combined_data.update(data)

        report = Report.objects.create(**combined_data)
        
        # If organization data is in session, create organization objects
        if 'organizations' in session_data:
            organizations_data = session_data['organizations']
            for org_data in organizations_data:
                Organization.objects.create(report=report, **org_data)

        images = request.FILES.getlist('image')
        for image in images:
            ReportImages.objects.create(report=report, image=image)

        files = request.FILES.getlist('file')
        for file in files:
            ReportFiles.objects.create(report=report, file=file)

        del request.session['form_data']
        return redirect('report_list')

    else:
        return redirect('create_report_step', step='basic')


def add_interest(request):
    """
    Handles the creation of a new Expression of Interest. This view initializes and validates
    the InterestForm. Upon validation, it associates the current user as the author, saves the form,
    and redirects to the initial landing page.
    """
    if request.method == 'POST':
        Interest_Form = InterestForm(request.POST)

        if Interest_Form.is_valid():
            interest = Interest_Form.save(commit=False)
            interest.author = request.user
            interest.save()
            return redirect('initial-landing')
    else:
        report_form = InterestForm()

    return render(request, 'unrce/eoi.html', {'form': InterestForm})


def contact(request):
    return render(request, 'unrce/contact.html')

@login_required
def report_list(request):
    """
    Lists all the Report objects authored by the currently logged-in user.
    Fetches and filters the Report objects by the current user and renders them in 'unrce/report_list.html'.
    """
    reports = Report.objects.filter(author=request.user)
    return render(request, 'unrce/report_list.html', {'reports': reports})

@login_required
def delete_image(request, image_id):
    """
    Allows users to delete images they have uploaded to reports
    """
    image = get_object_or_404(ReportImages, id=image_id)
    report = image.report
    if image.report.author == request.user:
        image.delete()
    return redirect('report_edit', report_id=report.id)



def users_list(request):
    users = User.objects.all().prefetch_related('groups', 'account')  
    context = {
        'users': users,
    }
    return render(request, 'unrce/users_list.html', context)

def report_review(request):
    """
    Lists all the Report objects available in the system, without filtering by author.
    Fetches all the Report objects and renders them in 'unrce/report_review.html'.
    """
    reports = Report.objects.filter()
    return render(request, 'unrce/report_review.html', {'reports': reports})

def report_details(request, report_id):
    """
    Lists the entire report for review, this is accessed from the report_review list of all reports
    """
    report = get_object_or_404(Report, id=report_id)
    report_form = ReportForm(instance=report)
    existing_images = ReportImages.objects.filter(report=report)
    
    context = {
        'form': report_form, 
        'existing_images': existing_images
    }
    return render(request, 'unrce/report_details.html', context)

def eoi_review(request):
    """
    Lists all the Report objects available in the system, without filtering by author.
    Fetches all the Report objects and renders them in 'unrce/report_review.html'.
    """
    eois = Expression_of_interest.objects.filter()
    return render(request, 'unrce/eoi_review.html', {'eois': eois})


@login_required
def report_edit(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    # Ensure the request.user is the author of the report or has permission
    if report.author != request.user:
        return redirect('report_list')

    try:
        if request.method == 'POST':
            report_form = ReportForm(request.POST, instance=report)
            images_form = ReportImagesForm(request.POST, request.FILES)
            files_form = ReportFilesForm(request.POST, request.FILES)
            organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
            images = request.FILES.getlist('image')
            files = request.FILES.getlist('file')

            if report_form.is_valid() and organization_formset.is_valid():
                report = report_form.save(commit=False)  # Do not save immediately

                # Capture the radio button selections for SDGs, ESD Themes, and Priority Areas
                direct_sdgs = []
                indirect_sdgs = []
                for i in range(1, 18):
                    option = request.POST.get(f'sdg_option_{i}')
                    if option == 'direct':
                        direct_sdgs.append(str(i))
                    elif option == 'indirect':
                        indirect_sdgs.append(str(i))

                direct_esd = []
                indirect_esd = []
                for theme in themes_esd:
                    option = request.POST.get(f'esd_theme_option_{theme}')
                    if option == 'direct':
                        direct_esd.append(theme)
                    elif option == 'indirect':
                        indirect_esd.append(theme)

                direct_priority = []
                indirect_priority = []
                for area in priority_action_areas:
                    option = request.POST.get(f'esd_priority_option_{area}')
                    if option == 'direct':
                        direct_priority.append(area)
                    elif option == 'indirect':
                        indirect_priority.append(area)

                report.direct_sdgs = direct_sdgs
                report.indirect_sdgs = indirect_sdgs
                report.direct_esd_themes = direct_esd
                report.indirect_esd_themes = indirect_esd
                report.direct_priority_areas = direct_priority
                report.indirect_priority_areas = indirect_priority
                linked_user_ids = request.POST.getlist('linked_users')
                report.linked_users.set(linked_user_ids)
                
                report.save()  # Now save after updating the above fields

                organization_formset.save()

                # Removing existing images/files and add new ones
                report.reportimages_set.all().delete()
                for image in images:
                    ReportImages.objects.create(report=report, image=image)

                report.reportfiles_set.all().delete()
                for file in files:
                    ReportFiles.objects.create(report=report, file=file)

                return redirect('report_list')
            else:
                for form in [report_form, images_form, files_form, organization_formset]:
                    if not form.is_valid():
                        logger.error(f'{form.__class__.__name__} errors: {form.errors}')

        else:
            report_form = ReportForm(instance=report)
            images_form = ReportImagesForm()
            files_form = ReportFilesForm()
            organization_formset = OrganizationInlineFormSet(instance=report)

        sdg_list = [str(i) for i in range(1, 18)]
        context = {
            'report': report,
            'report_form': report_form,
            'organization_formset': organization_formset,
            'images_form': images_form,
            'files_form': files_form,
            'sdg_list': sdg_list,
            'themes_esd': themes_esd,
            'priority_action_areas': priority_action_areas,
            'all_users': User.objects.all(),
            'linked_users': report.linked_users.all(),
            'existing_images': ReportImages.objects.filter(report=report),
            'existing_files': ReportFiles.objects.filter(report=report)
        }

        return render(request, 'unrce/report_edit.html', context)

    except Exception as e:
        # Logging the error for debugging
        logger.error(f'Error editing report: {str(e)}')
        return redirect('report_list')


def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                logging.debug("Form is valid")
                user = form.save()
                group, created = Group.objects.get_or_create(name='Visitor')
                user.groups.add(group)
                # Log in the user after registration if needed
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                logging.debug(f"Username: {username}, Password: {password}")
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    logging.debug("User logged in successfully")
                    return redirect('initial-landing')  # Redirect to a success page
                else:
                    logging.error("Authentication failed")  # Log authentication failure
                    return HttpResponseServerError("Authentication failed")  # Return an error response
    except Exception as e:
        logging.error(f"An exception occurred during registration: {str(e)}")  # Log the exception
        return HttpResponseServerError("An error occurred during registration")  # Return an error response

    # If the registration process was not successful, return the registration form
    form = RegistrationForm()
    return render(request, 'unrce/register.html', {'form': form})


@login_required
def profile(request):
    try:
        user = request.user  # Assuming you are using Django's authentication system
        account = Account.objects.get(user=user)  # Retrieve the Account associated with the user
    except Account.DoesNotExist:

        account = None
    return render(request, 'unrce/profile.html', {'user': user, 'account': account})

def must_be_signed_in(request):
    return render(request, 'unrce/redirect.html')


@login_required
def edit_reporting(request):
    return render(request, 'unrce/report_list.html')

@login_required
def reportDetails(request):
    return render(request, 'unrce/report_details.html')
from django.shortcuts import render

class ReportWizard(SessionWizardView):
    template_name = "report_wizard_form.html"
    file_storage = FileSystemStorage(location='/tmp/uploads')

    def done(self, form_list, **kwargs):
        # Here, add what you want to do with the data of all steps
        # For now, let's just render a 'done' template
        return render(self.request, 'done.html')

