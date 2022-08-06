# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 00:04:50 2020

@author: gjh56
"""
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# start of cool gamil libraries https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151
import os
import smtplib
import ssl
from email.message import EmailMessage


# def gmail_email(receiver_email, subject, message, img=None):
#     msg = MIMEMultipart('related')
#     msgText = MIMEText(message)
#     msg['Subject'] = subject
#     port = 465  # For SSL
#     smtp_server = "smtp.gmail.com"
#     sender_email = "hinglemc1738@gmail.com"  # Enter your address
#     password = "ThEhAnS125"
#     context = ssl.create_default_context()
    
#     if img:
#         # This example assumes the image is in the current directory
#         fp = open(img, 'rb')
#         msgImage = MIMEImage(fp.read())
#         fp.close()
        
#         # Define the image's ID as referenced above
#         msgImage.add_header('Content-ID', '<image1>')
#         msg.attach(msgImage)
#     else:
#         msg.attach(msgText)
        
#     for i in range (0,len(receiver_email)):
#         with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email[i], msg.as_string())
            



# cool tutorial

def gmail_email(receiver_email, subject, message, attachment=None, html=False):
    sender_email = "hinglemc1738@gmail.com"  # Enter your address
    app_password = os.environ.get('gmail_password')

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    if html:
        em.set_content(message, subtype='html')
    else:
        em.set_content(message)
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()

    # implement img attachment later, if desired
    # if img:
    #     # This example assumes the image is in the current directory
    #     fp = open(img, 'rb')
    #     msgImage = MIMEImage(fp.read())
    #     fp.close()
        
    #     # Define the image's ID as referenced above
    #     msgImage.add_header('Content-ID', '<image1>')
    #     em.attach(msgImage)
    # else:
    #     em.attach(em)

    for i in range (0,len(receiver_email)):
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email[i], em.as_string())

    