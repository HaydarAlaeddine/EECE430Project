from django.shortcuts import render, redirect

def index(request):
    return render(request,'base/homepage.html')