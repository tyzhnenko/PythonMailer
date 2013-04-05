# PythonMailer

Mailer module for Python. You can simply send email to your recipients

## Module Features

* Send mail to multiply To, Cc, Bcc
* Set own Message-id, Return-path
* Multipart/alternative
* Encoding emails by base64, 7 or 8 bit, quoted-printable

## Install

`$ git clone git://github.com/tyzhnenko/PythonMailer.git`

`$ sudo python setup.py install`

## Usage

### Make and send message with PythonMailer (simple example)
```
import PythonMailer

mailer = PythonMailer.PythonMailer()

rcpt = {
    "To": [{'email': 'jone@example.com', 'text': 'John'}],
}


mailer.setAddresess(rcpt)

mailer.setSender('jane@example.com')
mailer.setMessageId('test-mail@localhost.localdomain')
mailer.setSubject('Test subject')

senderOptions = {
    'Hostname': '127.0.0.1',
    'Port': 25,
    'Helo': 'localhost.localdomain'
}

mailer.Template = "Hello %name%,\nThis is test message\n\nWRB, %wbr%"
mailer.Replace({
    '%name%': 'John',
    '%wrb%': "Jane",
})

mailer.setMessageOptions(msgOptions)
mailer.setSenderOptions(senderOptions)

rcpt_ok, rcpt_false = mailer.Send()
```

## Roadmap

* Attachmets
* Background sending by threads
* DKIM 
* Relay mode. Sender can send message directly to MX