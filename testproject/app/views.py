from django.http import HttpResponse

from .models import ExampleModel


def home(_):
    return HttpResponse(str(list(ExampleModel.objects.all())))
