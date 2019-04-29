import logging
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import hashers
from django.db.models import Q

from login.forms import *
from login.models import *

# Create your views here.


def index(request):
    return render(request, 'index.html')


def logout(request):
    try:
        if request.session['remember']:
            del request.session['logged']
        else:
            request.session.flush()
        return HttpResponseRedirect('/')
    except:
        request.session.flush()
        return HttpResponseRedirect('/')


def login(request):
    form = LoginModel(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        player = Player.objects.get(playerMail__iexact=instance.playerMail)
        request.session['logged'] = 1
        request.session['player'] = player.playerName
        request.session['mail'] = player.playerMail
        if form.cleaned_data["rememberMe"]:
            request.session['remember'] = True
        else:
            request.session['remember'] = False
        logging.debug(form.cleaned_data["rememberMe"])
        return HttpResponseRedirect('/')
    else:
        try:
            if request.session['remember']:
                form.fields['playerMail'].initial = request.session['mail']
                form.fields['rememberMe'].initial = True
        except:
            pass
    return render(request, 'login.html', {'form': form})


def register(request):
    form = RefisterForm(request.POST or None)
    if form.is_valid():
        player = form.save()
        request.session['logged'] = 1
        request.session['player'] = player.playerName
        request.session['mail'] = player.playerMail
        request.session['remember'] = False
        player.password = hashers.make_password(player.password)
        player.save()
        return HttpResponseRedirect('/')
    return render(request, 'register.html', {'form': form})
