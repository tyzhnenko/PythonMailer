#!/usr/bin/python2.7 -d

# from PythonMailer import PythonMailer

from PythonMailer import MailerExceptions
import PythonMailer

mailer = PythonMailer.PythonMailer()

rcpt = {
    "To": [{'email': 'jone@example.com', 'text': 'Jone'}, {'email': 'jane@example.com', 'text': "Jane"}],
    "Cc": [{'email': 'jone_work@example.com', 'text': 'Jone Work'}],
    "From": [{'email': 'jones_mom@example.com', 'text': "Jone's Mom"}]
}

try:
    mailer.setAddresess(rcpt)
except Exception as e:
    print e.message
    exit(255)

mailer.setSender('jone_mom@example.com')
mailer.setMessageId('test-mail@localhost.localdomain')
mailer.setSubject('Test subject')

msgOptions = {
    "XMailer": "PythonMailer test",
    'Hostname': "localmachine.localdomain",
    'CharSet': "utf-8",
    'Encoding': "8bit",
    'Priority': 3,
}

senderOptions = {
    'Hostname': '127.0.0.1',
    'Port': 25,
    'Helo': 'localhost.localdomain'
}

mailer.Template = open('./example_body_template.txt')
mailer.TemplateType = 'text/html'
mailer.AltTemplate = open('./example_altbody_template.txt')
mailer.AltTemplateType = 'text/plain'
mailer.Replace({
    '%name%': 'Jone & Jane',
    '%site%': "Jone's Mom",
})

mailer.setMessageOptions(msgOptions)
mailer.setSenderOptions(senderOptions)

try:
    rcpt_ok, rcpt_false = mailer.Send()
except (MailerExceptions.SenderExeption, MailerExceptions.MessageExeption) as e:
    print e.message

mailer.Replace({
    '%name%': 'Jone 2 & Jane 2',
    '%site%': "Jone's Mom",
})

try:
    rcpt_ok, rcpt_false = mailer.Send()
except (MailerExceptions.SenderExeption, MailerExceptions.MessageExeption) as e:
    print e.message

mailer.Replace({
    '%name%': 'Jone 3 & Jane 3',
    '%site%': "Jone's Mom",
})

try:
    rcpt_ok, rcpt_false = mailer.Send()
except (MailerExceptions.SenderExeption, MailerExceptions.MessageExeption) as e:
    print e.message

print "Sended for:"
for e in rcpt_ok:
    print e['email']
print "Falied for:"
for e in rcpt_false:
    print e['email']
