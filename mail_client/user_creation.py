import os, django, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from mail.models import User, Mail
import random as rd
import string
from random import shuffle

n_users = 100

# Create an object for each email
zulily = {
    'sender': 'Zulily',
    'preview':'Daily Deals Up to 70%% Off Classic femininity meets modern romance in this ethereal collection of pieces delicately detailed with breezy lace and flouncy ruffles.',
    'subject':'Flowy Tunics & Dresses',
    'sender_address': 'mail-noreply@zulily.com',
    'ref': 1,
}

capone = {
    'sender': 'Capital One',
    'preview':'question about your account Visit Capital One Sign In Do you recognize this purchase? Re: Card ending in 3505,  Our fraud defenses flagged the purchase below as unusual for your MASTERCARD PLATINUM card ending in 3505. Do you or an authorized user recognize this purchase?',
    'subject':'Do you recognize this purchase? Re: Card',
    'sender_address': 'notification@capitalone.com',
    'ref': 2,
    'num_links': 3,
 }

chase  = {
     'sender': 'Chase Online',
     'preview':'We\'ve sent an important communication to your Secure Message Center, available on Chase Online or on the Chase Mobile app.  The subject is: New enhancements to your Chase QuickPay(R)  You can sign in to review this communication in your Secure Message Center until 09/24/2017.  Thank you for being a valued Chase customer.',
     'subject':'A secure message from Chase',
     'sender_address': 'no-reply@alertsp.chase.com',
     'ref': 3,
     'num_links': 2,
  }

usenix = {
    'sender': 'Usenix',
    'preview':'All student IDs that are on file with us will be expiring on September 1st. To continue receiving the benefits for full-time students, please sign into your account and upload your new ID at https://www.usenix.org/node/add/student-validation.',
    'subject':'Your Usenix student status will expire soon.',
    'sender_address': 'no-reply@usenix.com',
    'ref': 4,
}
archdigest = {
    'sender': 'Architectural Digest',
    'preview':'August 1, 2017 This Design Trick Will Open Up a Cramped Room Tree house vibes, here we come',
    'subject':'Cramped Room?  Open It Up With Design',
    'sender_address': 'email@archdigest.messages2.com',
    'ref': 5,
}
codeacademy = {
    'sender': 'Codeacademy',
    'preview':'View this email in your browser  NEWSLETTER #31 July 26, 2017 Announcing our newest free course - now you can make your websites look beautiful on any device, for free!',
    'subject':'New Free Course: Learn Responsive Design',
    'sender_address': 'contact@codeacademy.com',
    'ref': 6,
    'num_links': 2,
}
googledocs = {
    'sender': 'Google Docs',
    'preview':'Ronald Jameson has invited you to view the following document:  Assignment 7 Write Up Open in Docs',
    'subject':'Assignment 7 - Invitation to Edit',
    'sender_address': 'rjames@gmail.com',
    'ref': 7,
    'num_links': 3,
}
myspace = {
    'sender': 'Myspace Legal',
    'preview':'Notice of Data Breach You may have heard reports recently about a security incident involving Myspace. We would like to make sure you have the facts about what happened, what information was involved and the steps we are taking to protect your information.  What Happened? Shortly before the Memorial Day weekend (late May 2016), we became aware that stolen Myspace user login data was being made available in an online hacker forum. The data stolen included user login data from a portion of accoun',
    'subject':'Critical Information About Your Myspace Account',
    'sender_address': 'noreply@new.myspace.com',
    'ref': 8,
}
dropbox = {
    'sender': 'Dropbox',
    'preview':'Wilson has shared a folder (Last Semester Pictures) with you.  View Folder Now  Thank you! - The Dropbox Team.',
    'subject':'Wilson shared a folder',
    'sender_address': 'notifications@dropbox.com',
    'ref': 9,
}
facebook = {
    'sender': 'Facebook',
    'preview':'Hi, Your account was recently logged into from an unrecognized browser or device. Was this you?   New Login July 20, 2017 at 2:03pm Near Mumbai, India Chrome on Windows Review Login Manage Alerts',
    'subject':'Login alert for Chrome on Windows',
    'sender_address': 'security@facebookmail.com',
    'ref': 10,
    'num_links': 4,
}
humblebundle = {
    'sender': 'Humble Bundle',
    'preview':'Access the Humble Trove Subscribe to discover a treasure trove of games! Gain access to our full catalog of Humble Originals and other DRM-free gems Explore the Trove',
    'subject':'Subscribe to Humble Monthly!',
    'sender_address': 'contact@mailer.humblebundle.com',
    'ref': 11,
}
yahoo = {
    'sender': 'Yahoo',
    'preview':'Hello!  We have locked your account due to suspicious activity.  Please log in below to unlock your account: https://www.yahoo.com Thanks, Yahoo',
    'subject':'Security alert for your Yahoo account',
    'sender_address': 'no-reply@cc.yahoo-inc.com',
    'ref': 12,
    'num_links': 1,
}
mint = {
    'sender': 'Mint',
    'preview':'Hmm. We can\'t seem to connect with your Bank of America account We should be able to get you back on track pretty quickly. A reason for the glitch might be:      	Has your Bank of America login email or password changed?    Have they updated their security measures?    Do they require additional security questions?       The easiest way to fix it is to double-check and re-enter the most current login information you have for them.',
    'subject':'We\'re having a problem connecting with Bank of America',
    'sender_address': 'team@mint.com',
    'ref': 13,
    'num_links': 5,
}
scottrade = {
    'sender': 'Scottrade',
    'preview':'Dear Client,   The U.S. Postal Service (USPS) recently informed us of your new address. To be certain you don’t miss any account-related communication for your Scottrade®account, please complete the Contact Information Update form and return it to your local Scottrade® team or email the form to: support@scottrade.com. Additionally, you can update your information online by logging in to your account and following the path below:   My Account > My Information & Preferences > Contact Information',
    'subject':'Notice: Address Update Request',
    'sender_address': 'scottrade@e-mail.scottrade.com via responsys.net',
    'ref': 14,
}
amazon = {
    'sender': 'Amazon',
    'preview':'Order Confirmation Hello,  Thank you for shopping with us. You ordered 1 new item. We’ll send a confirmation when your items ship. Details',
    'subject':'Your Amazon.com order: 1 new item',
    'sender_address': 'auto-confirm@amazon.com',
    'ref': 15,
}
amex = {
    'sender': 'American Express',
    'preview':'No images? Please view in your browser for the full experience As a valued Gold Delta SkyMiles® Credit Card Card Member, you\'ve been selected for this special offer that can boost your SkyMiles® balance. For a limited time only, earn 25,000 bonus miles after you spend $2,000 or more in eligible purchases on the Platinum Delta SkyMiles® Credit Card within the first 3 months of Card Membership. 1 The annual membership fee for a Platinum Delta SkyMiles® Credit Card is $195.†2 Request an upgrade tod',
    'subject':'You\'re Eligible to Upgrade and Earn 25,000 Bonus Miles and Receive a Companion Certificate upon Renewal',
    'sender_address': 'americanexpress@member.americanexpress.com',
    'ref': 16,
}
aairlines = {
    'sender': 'American Airlines',
    'preview':'There are miles of opportunities awaiting View on the web American Airlines Claim your AAdvantage® miles today  Thanks for traveling with us.  You\'ve earned miles from your recent trip, but you\'ll need to set up an American Airlines AAdvantage® account to claim them. It\'s free and easy.',
    'subject':'Claim you AAdvantage miles now',
    'sender_address': 'AmericanAirlines@na.email.aa.com',
    'ref': 17,
}
venmo = {
    'sender': 'Venmo',
    'preview':'Hi,  Your transaction history for November 2017 is now available. View History on Venmo.com Venmo sends this notification periodically to help you stay on top of your account activity. Venmo is a service of PayPal, Inc., a licensed provider of money transfer services. All money transmission is provided by PayPal, Inc. pursuant to PayPal, Inc.\'s licenses.',
    'subject':'Your November 2017 Transaction History',
    'sender_address': 'venmo@venmo.com',
    'ref': 18,
    'num_links': 3,
}
linkedin = {
    'sender': 'LinkedIn',
    'preview':'We\'d like to help you  with your job search We invite you to try your Premium Job Seeker account - free! Here are just a few of the additional benefits you\'ll enjoy:',
    'subject':'Get a free trial of Premium Job Seeker',
    'sender_address': 'linkedin@e.linkedin.com',
    'ref': 19,
    'num_links': 7,
}
github = {
    'sender': 'GitHub',
    'preview':'GitHub, Inc Learn GitHub Flow Master the art of collaboration  The power of GitHub lies in the ability to work with others. GitHub Flow makes it easy for people to work together by simplifying how code changes are tracked, proposed, and merged. Check out our guide on GitHub Flow to learn more.',
    'subject':'Learn GitHub Flow',
    'sender_address': 'support@github.com',
    'ref': 20,
    'num_links': 4,
}

# We had 20 emails, but ended up using only 10
emails = [capone, chase, codeacademy, googledocs, facebook, yahoo, mint, github, venmo, linkedin]

# These are the dates each email displayed in the inbox
time_sent = ['Dec 1', 'Dec 6', 'Dec 7', 'Dec 9', 'Dec 10', 'Dec 12', 'Dec 14', 'Dec 17', 'Dec 18', 'Dec 23']

letter_pool = string.ascii_letters+'1234567890'
codelist = []

# Generate a random eight-string code
def generatecode():
    str_code = ''
    for i in range(8):
        str_code += rd.choice(letter_pool)
    return str_code

# Create a list of codes for each participant
while len(codelist) < n_users:
    code = generatecode()
    # Ensure no duplicate codes
    if code not in codelist:
        codelist.append(code)

# Generate the numbers to append to username
usernameNumbers = rd.sample(range(0,9999), n_users)

#initialize users
for i in range(0, n_users):
    shuffle(emails)
    user = User()
    # Initialize the numbers as usernameXXXX
    user.username = 'username{}'.format(usernameNumbers[i])
    # Assign to one of seven groups [0-6]
    user.condition_group = i % 7
    user.code = codelist[i]
    # user.set_password('pass1234')
    user.save()

    # This loop decrements so the dates append in the proper order
    # First email should have the last time_sent
    j=9 
    for email in emails:
        new = Mail()
        new.user = user
        new.sender = email['sender']
        new.preview = email['preview']
        new.time_sent = time_sent[j]
        new.subject = email['subject']
        new.sender_address = email['sender_address']
        new.read = "unread"
        new.ref = email['ref']
        new.num_links = email['num_links']
        new.save()
        j-=1

# Create a user to login into
# This helps with checking the inbox
user = User()
user.username = 'tempuser'
user.condition_group = 4
user.code = '432dsa4f'
### Set this password ###
user.set_password('SETPASSWORDHERE')
user.save()

j=9
for email in emails:
    new = Mail()
    new.user = user
    new.sender = email['sender']
    new.preview = email['preview']
    new.time_sent = time_sent[j]
    new.subject = email['subject']
    new.sender_address = email['sender_address']
    new.read = "unread"
    new.ref = email['ref']
    new.save()
    j-=1


exit()
