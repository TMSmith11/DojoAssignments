# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import User, Destination
from django.contrib import messages

# Create your views here.

def index(request):

    return render(request, 'index.html')

def login(request):

    errors_or_user = User.objects.validate_login(request.POST)
    if errors_or_user[0]:
        for fail in errors_or_user[0]:
            messages.error(request, fail)
        return redirect('/')

    request.session['id'] = errors_or_user[1].id
    print errors_or_user

    return redirect('/dashboard')

def register(request):
    errors_or_user = User.objects.validate_registration(request.POST)

    if errors_or_user[0]:
        for error in errors_or_user[0]:
            messages.error(request, error)
        return redirect('/')
    request.session['id'] = errors_or_user[1].id

    return redirect('/dashboard')


def dashboard(request):
    if not 'id' in request.session.keys():
         print 'no user'
         return redirect('/')
    inner_user = User.objects.get(id=request.session['id'])
    my_trips = inner_user.destinations.all()
    other_trips = Destination.objects.all().exclude(users=inner_user)
    context = {
        'user': inner_user,
        'trips': my_trips,
        'other_trips': other_trips
    }
    
    return render(request, 'dashboard.html', context)

def logout(request):
    del request.session['id']
    return redirect('/')

def destination(request, destination_id):
    inner_user = User.objects.get(id=request.session['id'])
    this_trip = Destination.objects.get(id=destination_id)
    details = this_trip
    travel_buddy = this_trip.users.all().exclude(id=request.session['id'])
    context ={
        'details': details,
        'travellers' : travel_buddy
    }
    
    return render(request, 'destination.html',context)

def add_travel(request):

    return render(request, 'add_travel.html')

def add(request): 
    errors_or_destination = Destination.objects.validate_destination(request.POST, request.session['id'])
    
    if errors_or_destination[0]:
        a = set(errors_or_destination[0])
        for error in errors_or_destination[0]:
            messages.error(request, error)
        return redirect('/add_travel')

    return redirect('/dashboard')

def join(request, destination_id):

    this_trip = Destination.objects.get(id=destination_id)
    current_user = User.objects.get(id=request.session['id'])
    current_user.destinations.add(this_trip)
    this_trip.users.add(current_user)
    
    return redirect('/dashboard')