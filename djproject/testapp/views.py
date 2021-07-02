from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from testapp.models import blorejobs, chennaijobs, hydjobs, punejobs, noidajobs

# Create your views here.
# This is Django version 3


def index(request):
    return render(request, 'testapp/index1.html')


def hydjobs1(request):
    jobs_list = hydjobs.objects.order_by('-date')
    paginator = Paginator(jobs_list, 25)
    page_number = request.GET.get('page')
    try:
        jobs_list = paginator.page(page_number)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return render(request, 'testapp/hydjobs.html', {'jobs_list': jobs_list})


def blorejobs1(request):
    #jobs_list = blorejobs.objects.order_by('-date')
    jobs_list = blorejobs.objects.order_by('-date')
    paginator = Paginator(jobs_list, 25)
    page_number = request.GET.get('page')
    try:
        jobs_list = paginator.page(page_number)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return render(request, 'testapp/blorejobs.html', {'jobs_list': jobs_list})


def punejobs1(request):
    jobs_list = punejobs.objects.order_by('-date')
    paginator = Paginator(jobs_list, 25)
    page_number = request.GET.get('page')
    try:
        jobs_list = paginator.page(page_number)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return render(request, 'testapp/punejobs.html', {'jobs_list': jobs_list})


def chennaijobs1(request):
    jobs_list = chennaijobs.objects.order_by('-date')
    paginator = Paginator(jobs_list, 25)
    page_number = request.GET.get('page')
    try:
        jobs_list = paginator.page(page_number)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return render(request, 'testapp/chennaijobs.html', {'jobs_list': jobs_list})


def noidajobs1(request):
    jobs_list = noidajobs.objects.order_by('-date')
    paginator = Paginator(jobs_list, 25)
    page_number = request.GET.get('page')

    try:
        jobs_list = paginator.page(page_number)
    except PageNotAnInteger:
        jobs_list = paginator.page(1)
    except EmptyPage:
        jobs_list = paginator.page(paginator.num_pages)
    return render(request, 'testapp/noidajobs.html', {'jobs_list': jobs_list})
