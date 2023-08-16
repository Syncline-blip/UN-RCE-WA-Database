from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReportForm

# sample data, not to be used, just for testing
project = [
    {
        'author': 'JOHN JOHN',
        'project': 'PROJECT LIVE',
        'project_code': 22341
    }
]
def home(request):
    return render(request, 'unrce/home_landing.html')

def projects(request):
    context = {
        'project': project
    }
    return render(request, 'unrce/project_upload.html', context)
# Create your views here.

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  
    else:
        form = ReportForm()

    return render(request, 'unrce/report_form.html', {'form': form})