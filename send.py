#!/usr/bin/python3
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from time import sleep
import os.path as osp


mail_host = 'smtp-tls.ie.cuhk.edu.hk'  # smtp server of your email
mail_host_port = 587
mail_user = 'hq016@ie.cuhk.edu.hk'  # username
mail_pass = '******'  # password

subject = 'Invitation to Hong Kong Computer Vision Workshop on October 12, 2019'


def send_one(title, name, email, bcc_list=[]):
    """
    param:
        title: title of the person you want to send
        name: full name of the person you want to send
        email: email of the person you want to send
    return:
        success or fail
    """

    # sender and receiver that show in the email
    # usually you will see sender_name<sender> and receiver_name<receiver> in the email
    sender = mail_user
    sender_name = sender[:sender.find('@')]
    receiver = email
    receiver_name = email[:email.find('@')]

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = formataddr([sender_name, sender])
    msgRoot['To'] = formataddr([receiver_name, receiver])
    if len(bcc_list) > 0:
        msgRoot['Bcc'] = ','.join([formataddr([x[:x.find('@')], x]) for x in bcc_list])

    # subject
    msgRoot['Subject'] = Header(subject)

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # add text
    family_name = name.split()[-1].strip()
    given_name = name.split()[0].strip()
    call = name
    with open('content.html', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('****', call)  # replace **** with family name in content

    message = MIMEText(text, 'html', 'utf-8')
    msgAlternative.attach(message)

    # send email
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_host_port)
        smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, [receiver,]+bcc_list, msgRoot.as_string())
        print(title + ' ' + name + ' success!')
    except smtplib.SMTPException:
        print(title + ' ' + name + ' fail!')
        return False
    return True


if __name__ == '__main__':
    # read bcc list if exist
    if osp.isfile('bcc.txt'):
        with open('bcc.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        bbc_list = [x.strip() for x in lines]
    else:
        bbc_list = []
    # read reveivers info
    with open('to.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    error_list = []
    for line in lines:
        # split title, name, email
        title, name, email = line.strip().split(',')
        # send an email
        flag = send_one(title, name, email, bbc_list)
        if not flag:
            error_list.append(line)
        sleep(1)
    if len(error_list) > 0:
        with open('error.txt', 'w') as f:
            for line in error_list:
                f.write(line)
