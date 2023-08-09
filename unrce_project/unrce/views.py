from django.shortcuts import render
from django.http import HttpResponse

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
