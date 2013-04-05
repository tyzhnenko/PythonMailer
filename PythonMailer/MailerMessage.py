"""Message module for PythonMailer
Wrapper to email python module
"""
from MailerExceptions import *

# from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders

import re
import time
import string
import math
import random


class MailerMessage(object):

    __version__ = '0.4'

    _Priority = 3

    _CharSet = 'utf-8'

    _Encoding = 'base64'

    _From = 'dev-null@localhost'

    _FromName = 'PythonMailer'

    _Sender = ''

    _ReturnPath = ''

    _Subject = ''

    _Recipients = {
        "To": [],
        "Cc": [],
        "Bcc": [],
    }

    _ReplyTo = ''

    _Body = ''

    _BodyType = 'text/html'

    _AltBody = ''

    _AltBodyType = 'text/plain'

    _MessageID = ''

    _MessageDate = ''

    _Hostname = 'localhost.localdomain'

    _XMailer = 'PythonMailer (%s)' % __version__

    _isCompile = False

    _ValidEmailRe = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$',
        re.IGNORECASE
    )

    _Message = None

    def __init__(self):
        pass

    def __str__(self):
        if self._isCompile is False:
            self.Compile()
        return self._Message.as_string(unixfrom=False)

    def getRecipients(self):
        """Fetch all recipients"""
        all_recipients = []
        for header in self._Recipients.keys():
            for addr in self._Recipients[header]:
                all_recipients.append(addr['email'])
        return all_recipients

    def uniqid(self, prefix='', more_entropy=False):
        """Make uniq id for message"""
        m = time.time()
        uniqid = '%8x%05x' % (math.floor(m), (m-math.floor(m)) * 1000000)
        if more_entropy:
            valid_chars = list(set(string.hexdigits.lower()))
            entropy_string = ''
            for i in range(0, 10, 1):
                entropy_string += random.choice(valid_chars)
            uniqid = uniqid + entropy_string
        uniqid = prefix + uniqid
        return uniqid

    def Compile(self):
        """Check message for error and compile it"""
        # self._Message = Message()
        self._Message = MIMEMultipart()
        m = self._Message
        if len(self._Body) == 0:
            raise EmptyBody("Please set Body")
        if len(self._Recipients['To']) + len(self._Recipients['Cc']) + len(self._Recipients['Bcc']) == 0:
            raise EmptyAddr("Recipients address not set")
        # if len(self._AltBody) > 0:
        #     self.ContentType = "multipart/alternative"
        if len(self._MessageDate) != 0:
            m.add_header("Date", self._MessageDate)
        else:
            m.add_header("Date", time.strftime("%a, %d %b %Y %T %z"))
        if len(self._ReturnPath) != 0:
            m.add_header("Return-path", self._ReturnPath)
        elif len(self._Sender) != 0:
            m.add_header("Return-path", self._Sender)
        else:
            m.add_header("Return-path", self._From)
            self._Sender = self._From

        for rcpt in self._Recipients.keys():
            if len(self._Recipients[rcpt]) > 0:
                for each in self._Recipients[rcpt]:
                    if len(each['text']) > 0:
                        m.add_header(rcpt, '"%s" <%s>' % (str(Header(each['text'], 'utf-8')), each['email']))
                    else:
                        m.add_header(rcpt, '<%s>' % (each['email']))
        if m.get("To") in (None, ''):
            m.add_header("To", 'undisclosed-recipients:;')
        m.add_header("From", self._From)

        if self._ReplyTo != '':
            reply_to = self._ReplyTo
            if len(reply_to['text']) > 0:
                m.add_header("Reply-To", '<%s>' (reply_to['email']))
            else:
                m.add_header("Reply-To", '"%s" <%s>' % (str(Header(reply_to['text'], 'utf-8')), reply_to['email']))

        if len(self._MessageID) != 0:
            m.add_header("Message-ID", self._MessageID)
        else:
            m.add_header("Message-ID", '<%s@%s>' % (self.uniqid(), self._Hostname))

        m.add_header('X-Priority', str(self._Priority))
        m.add_header("X-Mailer", self._XMailer)
        m.add_header("Subject", str(Header(self._Subject, 'utf-8')))


        if len(self._AltBody) > 0:
            # alt_body = MIMEText(self._AltBody, )
            # alt_body.set_type(self._AltBodyType)
            alt_body = MIMEBase(self._AltBodyType.split('/')[0], self._AltBodyType.split('/')[1])
            alt_body.set_payload(self._AltBody)
            if self._Encoding == 'base64':
                encoders.encode_base64(alt_body)
            elif self._Encoding == 'quoted':
                encoders.encode_quopri(alt_body)                
            elif self._Encoding in ('8bit', '7bit'):
                encoders.encode_7or8bit(alt_body)
            alt_body.set_charset(self._CharSet)

            # body = MIMEText(self._Body)
            # body.set_type(self._BodyType)
            body = MIMEBase(self._BodyType.split('/')[0], self._BodyType.split('/')[1])
            body.set_payload(self._Body)
            if self._Encoding == 'base64':
                encoders.encode_base64(body)
            elif self._Encoding == 'quoted':
                encoders.encode_quopri(body)
            elif self._Encoding in ('8bit', '7bit'):
                encoders.encode_7or8bit(body)            
            body.set_charset(self._CharSet)

            m.attach(alt_body)
            m.attach(body)
        else:
            # body = MIMEText(self._Body)
            # body.set_type(self._BodyType)
            body = MIMEBase(self._BodyType.split('/')[0], self._BodyType.split('/')[1])
            body.set_payload(self._Body)
            encoders.encode_base64(body)
            body.set_charset(self._CharSet)
            m.attach(body)

        # m.set_charset(self._CharSet)
        m.set_type('multipart/alternative')
        
        self._isCompile = True

    def AddTo(self, email, text=''):
        """Add recipient in To header"""
        self.AddAddress("To", email, text)

    def AddCc(self, email, text=''):
        """Add recipient in Cc header"""
        self.AddAddress("Cc", email, text)

    def AddBcc(self, email, text=''):
        """Add recipient in Bcc header"""
        self.AddAddress("Bcc", email, text)

    def AddReplyTo(self, email, text=''):
        """Add reply to address header"""
        self.AddAddress("ReplyTo", email, text)

    def AddAddress(self, where, email, text=''):
        if where in self._Recipients.keys() + ['ReplyTo']:
            email = email.strip('<> ').lower()
            if self.isEmailValid(email) is True:
                if where == "ReplyTo":
                    pass
                    self._ReplyTo = [{"email": email, "text": text}]
                else:
                    pass
                    if not any(i['email'] == email for i in self._Recipients[where]):
                        self._Recipients[where].append({'email': email, 'text': text})
            else:
                raise InvalidAddress("Please check email syntax")
                return False
        else:
            raise InvalidAddressHeader("Please set valid address header - " % ", ".join(self._Recipients.keys()))
            return False

    def isEmailValid(self, email):
        """Check email to valid"""
        if self._ValidEmailRe.match(email) is None:
            return False
        else:
            return True

    def ReturnPath():
        doc = "Set Return-path header."

        def fget(self):
            return self._ReturnPath

        def fset(self, value):
            if self.isEmailValid(value):
                self._ReturnPath = value.strip(' <>').lower()
            else:
                raise InvalidAddress('Please check email syntax for Return-path')
                return locals()

        def fdel(self):
            del self._ReturnPath
        return locals()
    ReturnPath = property(**ReturnPath())

    def Hostname():
        doc = "Set Hostname property."

        def fget(self):
            return self._Hostname

        def fset(self, value):
            self._Hostname = value

        def fdel(self):
            del self._Hostname
        return locals()
    Hostname = property(**Hostname())

    def XMailer():
        doc = "Set X-Mailer header."

        def fget(self):
            return self._XMailer

        def fset(self, value):
            value = value.strip()
            self._XMailer = value

        def fdel(self):
            del self._XMailer
        return locals()
    XMailer = property(**XMailer())

    def MessageID():
        doc = "Set Message-ID header."

        def fget(self):
            return self._MessageID

        def fset(self, value):
            value = value.strip()
            self._MessageID = value

        def fdel(self):
            del self._MessageID
        return locals()
    MessageID = property(**MessageID())

    def MessageDate():
        doc = "Set Date header."

        def fget(self):
            return self._MessageDate

        def fset(self, value):
            self._MessageDate = value

        def fdel(self):
            del self._MessageDate
        return locals()
    MessageDate = property(**MessageDate())

    def AltBody():
        doc = "Set message alternative body."

        def fget(self):
            return self._AltBody

        def fset(self, value):
            self._AltBody = value

        def fdel(self):
            del self._AltBody
        return locals()
    AltBody = property(**AltBody())

    def AltBodyType():
        doc = "Set alternative body content type."

        def fget(self):
            return self._AltBodyType

        def fset(self, value):
            self._AltBodyType = value

        def fdel(self):
            del self._AltBodyType
        return locals()
    AltBodyType = property(**AltBodyType())

    def Body():
        doc = "Set message body."

        def fget(self):
            return self._Body

        def fset(self, value):
            self._Body = value

        def fdel(self):
            del self._Body
        return locals()
    Body = property(**Body())

    def BodyType():
        doc = "Set body content type."

        def fget(self):
            return self._BodyType

        def fset(self, value):
            self._BodyType = value

        def fdel(self):
            del self._BodyType
        return locals()
    BodyType = property(**BodyType())

    def Subject():
        doc = "Set Subject header."

        def fget(self):
            return self._Subject

        def fset(self, value):
            value = value.strip()
            self._Subject = value

        def fdel(self):
            del self._Subject
        return locals()
    Subject = property(**Subject())

    def Sender():
        doc = "Set Sender address."

        def fget(self):
            return self._Sender

        def fset(self, value):
            value = value.strip()
            if self.isEmailValid(value):
                self._Sender = value
            else:
                raise InvalidAddress("Please check email syntax for Sender")
                return locals()

        def fdel(self):
            del self._Sender
        return locals()
    Sender = property(**Sender())

    def FromName():
        doc = "Set From text (ie. name)."

        def fget(self):
            return self._FromName

        def fset(self, value):
            value = value.strip()
            self._FromName = value

        def fdel(self):
            del self._FromName
        return locals()
    FromName = property(**FromName())

    def From():
        doc = "Set message From header (email)."

        def fget(self):
            return self._From

        def fset(self, value):
            value = value.strip()
            if self.isEmailValid(value):
                self._From = value
            else:
                raise InvalidAddress("Please check email syntax for From header")
                return locals()

        def fdel(self):
            del self._From
        return locals()
    From = property(**From())

    def Encoding():
        doc = "Set message Encoding (quoted, base64, 7 or 8 bit)."

        def fget(self):
            return self._Encoding

        def fset(self, value):
            value = value.strip()
            if value in ('base64', 'quoted', '7bit', '8bit'):
                self._Encoding = value
            else:
                self._Encoding = 'base64'
                

        def fdel(self):
            del self._Encoding
        return locals()
    Encoding = property(**Encoding())

    def Priority():
        doc = "Set message Priority."

        def fget(self):
            return self._Priority

        def fset(self, value):
            self._Priority = value

        def fdel(self):
            del self._Priority
        return locals()
    Priority = property(**Priority())

    def CharSet():
        doc = "Set message message charset."

        def fget(self):
            return self._CharSet

        def fset(self, value):
            value = value.strip()
            self._CharSet = value

        def fdel(self):
            del self._CharSet
        return locals()
    CharSet = property(**CharSet())
