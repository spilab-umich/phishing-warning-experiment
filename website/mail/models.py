from django.db import models
from django.contrib.auth.models import AbstractUser
import random


# Create your models here.
class User(AbstractUser):
    condition_group = models.IntegerField(blank = True, null=True)
    unread_count = models.IntegerField(default=10)
    assigned = models.BooleanField(default=False)
    response_id = models.CharField(default="0", max_length=50, null=True)
    code = models.CharField(default="Not Found", max_length=25)

    def __str__(self):
        return str(self.username) + ' - ' + str(self.condition_group)

class Mail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=250)
    preview = models.CharField(max_length=500, default='This is the preview text')
    time_sent = models.CharField(max_length = 20)
    subject = models.CharField(max_length = 250, default='This is the subject')
    sender_address = models.CharField(max_length = 50)
    read = models.CharField(max_length = 20, default='unread')
    ref = models.IntegerField(default=-1)
    num_links = models.IntegerField(default=-1)


    def __str__(self):
        return str(self.ref) + ' - ' + self.sender


class Logs(models.Model):
    username = models.CharField(max_length=50)
    link = models.CharField(max_length=500)
    client_time = models.CharField(max_length=100)
    server_time = models.CharField(max_length=100, null=True)
    condition_group = models.IntegerField(blank=True, null=True)
    response_id = models.CharField(default="0", max_length=50, null=True)
    session_id = models.CharField(default="0", max_length=50, null=True)
    screen_height = models.IntegerField(default=0)
    screen_width = models.IntegerField(default=0)
    statusbar_visible = models.CharField(null=True, max_length=20)
    action = models.CharField(max_length=20)
    #Server-side link_ids are -1
    #All email link_ids are > 0
    link_id = models.IntegerField(default=0)
    hover_time = models.IntegerField(default=-1)
    IP = models.CharField(null=True, max_length = 20)

    def __str__(self):
        return str(self.username) + ', ' + str(self.link) + ', ' + str(self.timestamp)
