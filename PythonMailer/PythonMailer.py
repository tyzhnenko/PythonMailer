
from MailerMessage import MailerMessage
from MailerSender import MailerSender


class PythonMailer(object):

    _Template = None

    _TemplateType = 'text/html'

    _Body = None

    _AltTemplate = None

    _AltTemplateType = 'text/plain'

    _AltBody = None

    _MSG = None

    _SENDER = None

    # _RCPTS = None

    def __init__(self):
        self._MSG = MailerMessage()
        self._SENDER = MailerSender()

    def __FillBody(self):
        """Set message bodt from templates"""
        if self._Body is None:
            self._MSG.Body = self._Template
        else:
            self._MSG.Body = self._Body
        self._MSG.BodyType = self._TemplateType
        if self._AltTemplate is not None:
            if self._AltBody is None:
                self._MSG.AltBody = self._AltTemplate
            else:
                self._MSG.AltBody = self._AltBody
            self._MSG.AltBodyType = self._AltTemplateType

    def Send(self):
        """Send message to server"""

        rcpt_ok = []
        rcpt_false = []
        self.__FillBody()
        self._MSG.Compile()
        # ret = self._SENDER.testSend(self._MSG)
        ret = self._SENDER.Send(self._MSG)
        for rcpt in ret:
            if rcpt['status'] == 'OK':
                rcpt_ok.append({'email': rcpt['email'], 'msg': rcpt['msg']})
            if rcpt['status'] == 'Failed':
                rcpt_false.append({'email': rcpt['email'], 'msg': rcpt['msg']})
        return rcpt_ok, rcpt_false

    def Replace(self, data=None):
        """Take a dict with replace patern, key - search patern, value - new string"""

        if self._Template is None or data is None:
            return False
        for key, value in data.iteritems():
            self._Body = self._Template.replace(key, value)
        if self._AltTemplate is not None:
            for key, value in data.iteritems():
                self._AltBody = self._AltTemplate.replace(key, value)
        return True

    def setAddresess(self, data):
        """Set address, From, To, Cc and Bcc headers"""

        if 'To' in data.keys():
            for to in data['To']:
                if 'text' in to.keys():
                    self._MSG.AddTo(to['email'], to['text'])
                else:
                    self._MSG.AddTo(to['email'])
        if 'Cc' in data.keys():
            for to in data['Cc']:
                if 'text' in to.keys():
                    self._MSG.AddCc(to['email'], to['text'])
                else:
                    self._MSG.AddCc(to['email'])
        if 'Bcc' in data.keys():
            for to in data['Bcc']:
                if 'text' in to.keys():
                    self._MSG.AddBcc(to['email'], to['text'])
                else:
                    self._MSG.AddBcc(to['email'])
        if 'From' in data.keys():
            for to in data['From']:
                if 'text' in to.keys():
                    self._MSG.From = to['email']
                    self._MSG.FromName = to['text']
                else:
                    self._MSG.From = to['email']

    def setSender(self, email):
        """Set sender address, like sendmail -f"""

        self._MSG.Sender = email

    def setReturnPath(self, email):
        """Set Return-path header"""

        self._MSG.ReturnPath = email

    def setMessageId(self, value):
        """Set Message-ID header"""

        self._MSG.MessageId = value

    def setSubject(self, value):
        """Set subject for message"""

        self._MSG.Subject = value

    def setMessageOptions(self, value=None):
        """Setup message headeres, X-Mailer, Chatset, Encoding, X-Mailer and Hostname"""

        if value is not None:
            if 'Hostname' in value.keys():
                self._MSG.Hostname = value['Hostname']
            if 'XMailer' in value.keys():
                self._MSG.XMailer = value['XMailer']
            if 'CharSet' in value.keys():
                self._MSG.CharSet = value['CharSet']
            if 'Encoding' in value.keys():
                self._MSG.Encoding = value['Encoding']
            if 'Priority' in value.keys():
                self._MSG.Priority = value['Priority']
        else:
            return False

    def setSenderOptions(self, value=None):
        """Set sender params, Hostname, Port, Helo, AuthUser and AuthPwd"""

        if value is not None:
            if 'Hostname' in value.keys():
                self._SENDER.SMTPHostname = value['Hostname']
            if 'Port' in value.keys():
                self._SENDER.SMTPPost = value['Port']
            if 'Helo' in value.keys():
                self._SENDER.SMTPHelo = value['Helo']
            if 'AuthUser' in value.keys():
                self._SENDER.SMTPAuthUser = value['AuthUser']
                self._SENDER.SMTPAuthPwd = value['AuthPwd']
        else:
            return False

    def TemplateType():
        doc = "Set TemplateType default is text/html."

        def fget(self):
            return self._TemplateType

        def fset(self, value):
            self._TemplateType = value

        def fdel(self):
            del self._TemplateType
        return locals()
    TemplateType = property(**TemplateType())

    def Template():
        doc = "Set Template for message body, accept file or string"

        def fget(self):
            return self._Template

        def fset(self, value):
            if isinstance(value, file):
                new_value = value.read()
                self._Template = new_value
            else:
                self._Template = value

        def fdel(self):
            del self._Template
        return locals()
    Template = property(**Template())

    def AltTemplate():
        doc = "Set TemplateType default is text/plain."

        def fget(self):
            return self._AltTemplate

        def fset(self, value):
            if isinstance(value, file):
                new_value = value.read()
                self._AltTemplate = new_value
            else:
                self._AltTemplate = value

        def fdel(self):
            del self._AltTemplate
        return locals()
    AltTemplate = property(**AltTemplate())

    def AltTemplatyType():
        doc = "Set alternative template for alternative body, accept file or string"

        def fget(self):
            return self._AltTemplatyType

        def fset(self, value):
            self._AltTemplatyType = value

        def fdel(self):
            del self._AltTemplatyType
        return locals()
    AltTemplatyType = property(**AltTemplatyType())
