"""Sender module for PythonMailer
Send message(MailerMessage) to smtp server
Wrapper for smptlib python module
"""

from MailerExceptions import *

import smtplib
# import PythonMailerMessage

__version__ = '0.4'


class MailerSender(object):

    # Choose smtp, smtps, lmtp
    _Mailer = 'smtp'

    _SMTPHostname = 'localhost.localdomain'

    _SMTPPort = 25

    _SMTPHelo = None

    _SMTPAuthUser = None

    _SMTPAuthPwd = None

    _SMTPTimeout = '10'

    _DKIMSelector = None

    _DKIMIdentity = None

    _DKIMPrivate = None

    _DKIMDomain = None

    _SMTP = None

    def __init__(self):
        pass

    def __del__(self):
        if isinstance(self._SMTP, smtplib.SMTP) or isinstance(self._SMTP, smtplib.SMTP_SSL) or isinstance(self._SMTP, smtplib.LMTP):
            self._SMTP.close()

    def Connect(self):
        """Make connection to smtp server"""
        if self._SMTP is None:
            if self._Mailer == 'smtp':
                self._SMTP = smtplib.SMTP()
                self._SMTP.set_debuglevel(100)
            elif self._Mailer == 'smtps':
                self._SMTP = smtplib.SMTP_SSL()
            elif self._Mailer == 'lmtp':
                self._SMTP = smtplib.LMTP()

        if not self.isConnected():
            self._SMTP.connect(self._SMTPHostname, self._SMTPPort)
            if self._SMTPHelo is not None:
                self._SMTP.local_hostname = self._SMTPHelo
            if self._SMTPAuthUser is not None:
                self._SMTP.login(self._SMTPAuthUser, self._SMTPAuthPwd)

    def testSend(self, message):
        """Test sending and return recipients list with status"""
        print "Connect to MTA"
        mail_from = message.Sender
        rcpts = message.getRecipients()
        if len(rcpts) == 0:
            raise SendingError("Recipients is empty")
        print "mail FROM: %s" % mail_from

        rcpt_status = []
        for rcpt in rcpts:
            print "mail TO: %s" % rcpt
            rcpt_status.append({'email': rcpt, 'status': 'OK', 'msg': 'Test send OK'})

        print "data\r\n%s\r\n.\r\n" % str(message)
        return rcpt_status

    def Send(self, message):
        """Send message to SMTPHostname and return recipients list with status"""
        if not self.isConnected():
            self.Connect()
        mail_from = message.Sender
        rcpts = message.getRecipients()
        if len(rcpts) == 0:
            raise SendingError("Recipients is empty")

        (code, resp) = self._SMTP.mail(mail_from)
        if code != 250:
            self._SMTP.rset()
            raise SendingError("Sender not set. Code: %i, msg: %s" % (code, resp))

        rcpt_status = []
        for rcpt in rcpts:
            (code, resp) = self._SMTP.rcpt(rcpt)
            if code == 250:
                rcpt_status.append({'email': rcpt, 'status': 'OK', 'msg': resp})
            else:
                rcpt_status.append({'email': rcpt, 'status': 'Failed', 'msg': resp})

        try:
            (code, resp) = self._SMTP.data(str(message))
        except smtplib.SMTPDataError as e:
            #if isinstance(e, smtplib.SMTPDataError):
            self._SMTP.rset()
            rcpt_status = []
            raise SendingError('Server not accept message (DATA cmd). Code: %i, msg: %s, err: %s' % (code, resp, e.message))
        if code != 250:
            raise SendingError('Server not accept message (DATA cmd). Code: %i, msg: %s' % (code, resp))

        return rcpt_status

    def isConnected(self):
        """Check connection to smtp server return bool"""
        if self._SMTP is None:
            return False
        try:
            self._SMTP.noop()
        except Exception as e:
            if isinstance(e, smtplib.SMTPServerDisconnected):
                return False
        else:
            return True

    def Mailer():
        doc = "Set and get a mailer (smtp, ssmtp, lmtp) default is smtp."

        def fget(self):
            return self._Mailer

        def fset(self, value):
            self._Mailer = value

        def fdel(self):
            del self._Mailer
        return locals()
    Mailer = property(**Mailer())

    def SMTPHostname():
        doc = "Set and get connections hostname ."

        def fget(self):
            return self._SMTPHostname

        def fset(self, value):
            self._SMTPHostname = value

        def fdel(self):
            del self._SMTPHostname
        return locals()
    SMTPHostname = property(**SMTPHostname())

    def SMTPPort():
        doc = "Set and get connection port."

        def fget(self):
            return self._SMTPPort

        def fset(self, value):
            self._SMTPPort = value

        def fdel(self):
            del self._SMTPPort
        return locals()
    SMTPPort = property(**SMTPPort())

    def SMTPHelo():
        doc = "Set and get smtp Helo message."

        def fget(self):
            return self._SMTPHelo

        def fset(self, value):
            self._SMTPHelo = value

        def fdel(self):
            del self._SMTPHelo
        return locals()
    SMTPHelo = property(**SMTPHelo())

    def SMTPAuthUser():
        doc = "Set and get smtp auth user name."

        def fget(self):
            return self._SMTPAuthUser

        def fset(self, value):
            self._SMTPAuthUser = value

        def fdel(self):
            del self._SMTPAuthUser
        return locals()
    SMTPAuthUser = property(**SMTPAuthUser())

    def SMTPAuthPwd():
        doc = "Set and get smtp auth password."

        def fget(self):
            return self._SMTPAuthPwd

        def fset(self, value):
            self._SMTPAuthPwd = value

        def fdel(self):
            del self._SMTPAuthPwd
        return locals()
    SMTPAuthPwd = property(**SMTPAuthPwd())

    def SMTPTimeout():
        doc = "Set and get smtp connection timeout."

        def fget(self):
            return self._SMTPTimeout

        def fset(self, value):
            self._SMTPTimeout = value

        def fdel(self):
            del self._SMTPTimeout
        return locals()
    SMTPTimeout = property(**SMTPTimeout())

    def DKIMSelector():
        doc = "Set and get DKIM Selector."

        def fget(self):
            return self._DKIMSelector

        def fset(self, value):
            self._DKIMSelector = value

        def fdel(self):
            del self._DKIMSelector
        return locals()
    DKIMSelector = property(**DKIMSelector())

    def DKIMIdentify():
        doc = "Set and get DKIM Identify."

        def fget(self):
            return self._DKIMIdentify

        def fset(self, value):
            self._DKIMIdentify = value

        def fdel(self):
            del self._DKIMIdentify
        return locals()
    DKIMIdentify = property(**DKIMIdentify())

    def DKIMPrivate():
        doc = "Set and get DKIM Private."

        def fget(self):
            return self._DKIMPrivate

        def fset(self, value):
            self._DKIMPrivate = value

        def fdel(self):
            del self._DKIMPrivate
        return locals()
    DKIMPrivate = property(**DKIMPrivate())

    def DKIMDomain():
        doc = "Set and get DKIM Domain."

        def fget(self):
            return self._DKIMDomain

        def fset(self, value):
            self._DKIMDomain = value

        def fdel(self):
            del self._DKIMDomain
        return locals()
    DKIMDomain = property(**DKIMDomain())
