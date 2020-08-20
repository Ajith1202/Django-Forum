from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def list_view(request):
    queryset = Post.objects.all()
    return HttpResponse(queryset)