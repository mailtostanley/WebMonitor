#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import encoders
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr
from email.utils import formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendEmail(message):
    msg = MIMEText(message, 'plain', 'utf-8')
    fromAddr = "devtest@sensoro.com"
    toAddrList = []
    if __debug__:
        toAddrList.append("feng.liu@sensoro.com")
    else:
        toAddrList.append("feng.liu@sensoro.com")
        toAddrList.append("huiter@sensoro.com")
        toAddrList.append("limjoe@sensoro.com")
        toAddrList.append("leaf@sensoro.com")
    smtpServer = "smtp.exmail.qq.com"
    password = "Sensoro15"
    msg['From'] = _format_addr(u'Sensoro Monitor Program <%s>' % fromAddr)
    # msg['To'] = _format_addr(u'Sensoro Team <%s>' % toAddr)
    msg['Subject'] = Header(
        u'Web API Error from SensoroMonitor', 'utf-8').encode()
    server = smtplib.SMTP(smtpServer, 25)
    server.set_debuglevel(1)
    server.login(fromAddr, password)
    server.sendmail(fromAddr, toAddrList, msg.as_string())
    server.quit()

if __name__ == '__main__':
    sendEmail("this is a test.")