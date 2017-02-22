from django.shortcuts import render

# Create your views here.


def index(request):
    # just to check if template works
    return render(request,'activity/create.html')