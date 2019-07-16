from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
import random, logging, json
from datetime import datetime, timezone
from mail.models import Logs

# This code redirects requests to our phishing sites to the legit sites
# For security reasons, we have omitted the links 
def webpage(request):
    host = request.get_host()
    # Input allowed hosts below
    allowed_hosts = ['']
    if host == 'maindomain.com':
        return redirect('mail:index')
    elif host in allowed_hosts:
        if host in allowed_hosts[:2]:
            log_phish(request)
            return redirect('legit site #1')
        elif host in allowed_hosts[2:4]:
            log_phish(request)
            return redirect('legit site #2')
        elif host in allowed_hosts[4:]:
            log_phish(request)
            return redirect('legit site #3')
    return HttpResponse(host)

# Make logs on the server side
def log_phish(request):
    log = Logs()
    if (request.META.get('REMOTE_ADDR')):
        log.IP = request.META.get('REMOTE_ADDR')
    log.link = request.build_absolute_uri()
    log.link_id = -1
    log.server_time = datetime.now(timezone.utc).strftime("%a, %d %B %Y %H:%M:%S GMT")
    log.action = 'serverlog'
    try:
        log.session_id = request.session.session_key
    except:
        log.session_id = request.META.get('HTTP_COOKIE')
        pass
    try:
        log.response_id = request.user.response_id
    except:
        pass
    # Sun, 28 Jan 2018 04:05:02 GMT
    try:
        log.condition_group = request.user.condition_group
    except:
        pass
    log.save()
