from django.shortcuts import render

# Create your views here.
from .models import Features

def index(request):
    """View function for home page of site."""

    num_features = Features.objects.all().count()

    context = {'num_features':num_features}

    # Render the HTML template index.html with the data in the context variable
    return render(request,'index.html',context=context)

# def login(request):
#     """View function for login page."""

#     return render(request, 'login.html')

# def signup(request):
#     """View function for signup page."""

#     return render(request, 'signup.html')

# def dashboard(request):
#     """View function for user dashboard page."""

#     return render(request, 'dashboard.html')