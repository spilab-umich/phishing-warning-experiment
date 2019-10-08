from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Mail, User, Logs
from django.http import JsonResponse, HttpResponse
# Imported this so I can increment unread_count in the email view
from django.db.models import F
import random as rd, logging, json
from random import shuffle
from datetime import datetime, timezone
import string

#login view
def index(request):
    #if the request is POST, authenticate the user's credentials
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #sometimes you need to ban or restrict users
            if user.is_active:
                login(request, user)
                #send an authenticated, active user and their randomized emails to the inbox
                return redirect('mail:inbox')
            else:
                return render(request, 'mail/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'mail/index.html', {'error_message': 'Invalid login'})

    #if the request is not POST, render the index(login) page
    return render(request, 'mail/index.html')


#inbox view
def inbox(request):
    #bounce the request if the user is not authenticated
    if not request.user.is_authenticated:
        return redirect('mail:index')
    else:
        #log the request on the server side
        log_request(request)
        user = request.user
        emails = Mail.objects.filter(user=user).values()
        context = {
            'user': user,
            'emails': emails,
        }
        return render(request, 'mail/inbox.html', context)

#~mail/email/email_id
#individual email view
def email(request, email_id):
    #bounce the request if the user is not authenticated
    if not request.user.is_authenticated:
        return redirect('mail:index')
    else:
        #log the request on the server side
        log_request(request)
        #query the requisite email from the database
        user = request.user
        # Get a dictionary list of all mail objects belonging to this user
        emails = Mail.objects.filter(user=user).values()
        # Evaluate the query set (hit the database)
        len_emails = len(emails) - 1
        # Grab db ids for the first and last emails for this user
        first_id = emails[0]['id']
        last_id = emails[len_emails]['id']
        # Find the index of the matching email in emails
        this_index=0
        # Go through the query set and find the db id for the email id
        for mail in emails:
            if mail.get("ref") == int(email_id):
                this_id = mail.get("id")
                read_status = mail.get("read")
                # Once the id is found, we don't need to keep looking
                break
            this_index += 1
        # See if the next id is out of bounds
        if (this_id+1 > last_id):
            # Set to -1
            next_email = -1
        # Else set this to the next email ref number
        else:
            next_email = emails[this_index+1]["ref"]
        # See if the prev id is out of bounds
        if (this_id-1 < first_id):
            # Set to -1
            prev_email = -1
            # Else set this to the next email ref number
        else:
            prev_email = emails[this_index-1]["ref"]

        #path to each email (templates/mail/<email_id>.html)
        file_name = 'mail/emails/' + str(email_id) + '.html'

        # If unread, change to read, decrement unread_count, and save
        if read_status == "unread":
            Mail.objects.filter(user=user, ref=email_id).update(read="read")
            # this_mail.read="read"
            # user.unread_count -=1
            User.objects.filter(username=user.username).update(unread_count=F("unread_count")-1)
            if user.unread_count > 0:
                user.unread_count -= 1
        context = {
            'email': emails[this_index],
            'user': user,
            'file_name': file_name,
            'next_email': next_email,
            'prev_email': prev_email,
        }
        return render(request, 'mail/email.html', context)

def logout_user(request):
    log_request(request)
    logout(request)
    return redirect('mail:index')

def assign_password():
    str_code = ''
    letter_pool = string.ascii_letters+'1234567890'
    for i in range(8):
        str_code += rd.choice(letter_pool)
    return str_code

# Receive the request from Qualtrics after informed consent
def assign_credentials(request):
    if request.method == "GET":
        # Return a list of the remaining available usernames
        users = User.objects.filter(assigned=False).filter(is_superuser=False)
        # users is a QuerySet. Calling len() on users caches the whole database at once
        # This avoids multiple db calls
        len_users = len(users)
        if len_users < 1:
            username = 'Available user names depleted. Please contact investigators.'
            password = ''
        else:
            # Choose a random available username
            # Try it twice just in case.
            try:
                user_index = rd.randint(0,len_users-1)
                user = users[user_index]
            except:
                user_index = rd.randint(0,len_users-1)
                user = users[user_index]
            # Save the response_id from Qualtrics
            if (request.META.get("HTTP_RESPONSEID")):
                user.response_id = request.META.get("HTTP_RESPONSEID")
            username = user.username
            password = assign_password()
            # Mark the username as 'assigned'
            user.assigned = True
            user.set_password(password)
            user.save()
            condition_group = user.condition_group
            code = user.code
        context = {
            'username': username,
            'password': password,
            'condition_group': condition_group,
            'code': code,
        }
        return JsonResponse(context)

# Make logs on the server side
def log_request(request):
    log = Logs()
    log.username = request.user.username
    log.link = request.path
    log.link_id = -1
    log.server_time = datetime.now(timezone.utc).strftime("%a, %d %B %Y %H:%M:%S GMT")
    log.action = 'serverlog'
    log.session_id = request.session.session_key
    log.response_id = request.user.response_id
    # Sun, 28 Jan 2018 04:05:02 GMT
    log.condition_group = request.user.condition_group
    if (request.META.get('REMOTE_ADDR')):
        log.IP = request.META.get('REMOTE_ADDR')
    log.save()

def receiver(request):
    if request.method == 'POST':
        log = Logs()
        # Grab parts of the POST header we are sending
        log.username = request.POST['username']
        log.link = request.POST['link']
        log.link_id = request.POST['link_id']
        log.action = request.POST['action']
        log.hover_time = request.POST['hover_time']
        log.screen_width = request.POST['screen_width']
        log.screen_height = request.POST['screen_height']
        log.statusbar_visible = request.POST['statusbar_visible']
        log.client_time = request.POST['client_time']
        log.condition_group = request.user.condition_group
        log.response_id = request.user.response_id
        log.server_time = datetime.now(timezone.utc).strftime("%a, %d %B %Y %H:%M:%S GMT")
        log.session_id = request.session.session_key
        if (request.META.get('REMOTE_ADDR')):
            log.IP = request.META.get('REMOTE_ADDR')
        log.save()
    return HttpResponse('')
