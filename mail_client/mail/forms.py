#base user class
from django.contrib.auth.models import User
#make new User form class
from django import forms
import random

class UserForm(forms.ModelForm):
    #keeps the password hidden
    password = forms.CharField(widget=forms.PasswordInput)
    condition_group = forms.IntegerField(widget=forms.NumberInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'condition_group']


    def __str__(self):
        return(self.fields)
