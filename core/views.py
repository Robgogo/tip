from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, "build/index.html")


def bad_request(request, exception):
    return redirect(reverse('index'))
