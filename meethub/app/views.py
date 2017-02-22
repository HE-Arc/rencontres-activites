from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


def index(request):
    # just to check if template works
    return render(request,'activity/create.html')


class Activity(View):
    def get(self, request):
        return HttpResponse("GET")

    def post(self, request):
        return HttpResponse("POST")