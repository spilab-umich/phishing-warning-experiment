# phishing-warning-experiment
Code and supplemental materials for the CHI 2019 phishing warning experimental study.

Justin Petelka, Yixin Zou, and Florian Schaub
Put Your Warning Where Your Link Is: Improving and Evaluating Email Phishing Warnings
CHI Conference on Human Factors in ComputingSystems Proceedings (CHI 2019)
May 4–9, 2019, Glasgow, Scotland, UK. ACM, New York, NY, USA. 
https://doi.org/10.1145/3290605.3300748

## Installation
There are two folders in our repo, **analysis** and **mail_client**. 

### analysis
This contains the script we used to analyze our data. We have provided both the original .RMD files and pdf versions.

### mail_client
This is our website/mail-client, developed using Django 1.11. These instructions do not walk through how to set up an entire webserver, but we do provide several resources to help setup below:

[Setting up a webserver (Apache and Ubuntu 16.04)](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-16-04)

[Configuring your webserver to serve Django applications (Apache, Ubuntu 16.04, and mod_wsgi](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04)


[Installing Django and creating a project](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)

 The **mail** module in the **mail_client** folder is our mail client, while the **website** folder handled requests to our top-level domains. We include the **website** folder as an example, but ultimately you will have to configure your own **website** folder as appropriate to your hosting situation.
 
Once you have a Django project deployed on a host, you can import the mail module with the following commands in your Terminal:
- python manage.py makemigrations mail
- python manage.py sqlmigrate mail 0001
- python manage.py migrate mail
