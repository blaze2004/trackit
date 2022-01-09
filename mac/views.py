from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request,'index.html')

@login_required
def dashboard(request):
    """View function for user dashboard page."""

    return render(request, 'dashboard.html')