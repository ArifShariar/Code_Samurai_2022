from django.shortcuts import render
from django.http import HttpResponse

from CsvParser.utils import *


def index(request):
    ret = parseCsv(CONSTRAINTS)
    return HttpResponse("CsvParser")
