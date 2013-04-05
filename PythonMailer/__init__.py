# Copyright (C) 2013 Tyzhnenko Dmitry
# Author: Tyzhnenko Dmitry
# Contact: t.dmitry@gmail.com
"""Simple mail module for Python. 
Make message with PythonMailer.MailerMessage and send it via PythonMailer.MailerSender
"""

__version__ = '0.4'

__all__ = ['PythonMailer', 'MailerSender', 'MailerMessage']

import PythonMailer

PythonMailer = PythonMailer.PythonMailer
