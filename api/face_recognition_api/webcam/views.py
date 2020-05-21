from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = get_template('')
    return HttpResponse(template.render({}, request))

# Create your views here.
