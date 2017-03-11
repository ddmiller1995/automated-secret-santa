# Author: Dakota Miller
# Created: December 2016
# Simple automated secret santa, so the author can participate!
# Generates pairings and send them out via email.

import smtplib
import json
import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# See data file for expected json formatting
with open('data.json') as data_file:
    data = json.load(data_file)

matches = {}
givers = list(data.keys())
receivers = list(data.keys())

# Generate giver-receiver pairs, making sure no one is assigned to themselves
# and that there are no symmetric pairings
for email in givers:
    choice = random.choice(receivers)
    while choice == email or (choice in matches and matches[choice] == email):
        choice = random.choice(receivers)
    matches[email] = choice
    receivers.remove(choice)

# Organizer's email here
me = "email@gmail.com"
# Send the message via email survey, set to gmail.
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()

# Login to email server, gmail works if security alert email overridden
s.login("email", "password")

# Generate an send the emails
for email in matches:
    giv_name = data[email]["Name"]
    rec_email = matches[email]
    rec_name = data[rec_email]["Name"]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Secret Santa Assignment"
    msg['From'] = me
    msg['To'] = you #email

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nYour Secret Santa Assignment is: " + rec_name + "\nTheir interests can be found in this spreadsheet: " \
                                                                 "Signup survey responses URL"
    html = """\
    <html>
        <head></head>
        <body style="font-size: 14pt;font-family: Helvetica, sans-serif;color: #444;">
            <style type="text/css">
                body {
                    font-size: 14pt;
                    font-family: Helvetica, sans-serif;
                    color: #444;
                }

                h1 {
                    color: green;
                }

                table {
                    border: 3px double #ccc;
                    padding: 0.5em;
                }

                td {
                    padding: 0.5em;
                    vertical-align: top;
                }

                td:first-of-type {
                    width: 200px;
                    text-align: right;
                    font-weight: bold;
                    color: green;
                }

                td:nth-of-type(2) {
                    width: 500px;
                }

            </style>
            <img style="width: 816px;" src="http://i.imgur.com/jRTYNei.jpg">
            <h1 style="color: green;">Hi """ + giv_name + """!</h1>
            <p>Your Secret Santa Assignment is <strong>""" + rec_name + """</strong><br>
                Please get a $10-$20 gift for them before Friday, December 9th. Below is their interests survey responses
            </p>
            <table style="border: 3px double #ccc;padding: 0.5em;">
                <tr>
                    <td style="padding: 0.5em;vertical-align: top;width: 250px;text-align: right;font-weight: bold;color: green;">Name:</td>
                    <td style="padding: 0.5em;vertical-align: top;width: 500px;">""" + rec_name + """</td>
                </tr>
                <tr>
                    <td style="padding: 0.5em;vertical-align: top;width: 250px;text-align: right;font-weight: bold;color: green;">Favorite Food / Candy:</td>
                    <td style="padding: 0.5em;vertical-align: top;width: 500px;">""" + data[rec_email]["Favorite Food / Candy"] + """</td>
                </tr>
                <tr>
                    <td style="padding: 0.5em;vertical-align: top;width: 250px;text-align: right;font-weight: bold;color: green;">Favorite Movie:</td>
                    <td style="padding: 0.5em;vertical-align: top;width: 500px;">""" + data[rec_email]["Favorite Movie"] + """</td>
                </tr>
                <tr>
                    <td style="padding: 0.5em;vertical-align: top;width: 250px;text-align: right;font-weight: bold;color: green;">Favorite Color:</td>
                    <td style="padding: 0.5em;vertical-align: top;width: 500px;">""" + data[rec_email]["Favorite Color"] + """</td>
                </tr>
                <tr>
                    <td style="padding: 0.5em;vertical-align: top;width: 250px;text-align: right;font-weight: bold;color: green;">Favorite Hobbies:</td>
                    <td style="padding: 0.5em;vertical-align: top;width: 500px;">""" + data[rec_email]["Favorite Hobbies"] + """</td>
                </tr>
                <tr>
                    <td style="padding: 0.5em;vertical-align: top;width: 250px;text-align: right;font-weight: bold;color: green;">Other Interests / Things you want:</td>
                    <td style="padding: 0.5em;vertical-align: top;width: 500px;">""" + data[rec_email]["Other interests / Things you want"] + """</td>
                </tr>
            </table>
        </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)


    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, email, msg.as_string())

s.quit()