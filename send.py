#!/usr/bin/python3
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from time import sleep

mail_host = 'smtp.domain.com'  # smtp server of your email
mail_host_port = 25
mail_user = 'asia-night-2017@ijcvasia.org'  # username
mail_pass = '****'  # password

subject = 'IJCV Asia Night Invitation'


def send_one(title, name, email):
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

    # subject
    msgRoot['Subject'] = Header(subject)

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # add text
    family_name = name.split()[-1].strip()
    call = title + ' ' + family_name
    with open('content.html', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('****', call)  # replace **** with family name in content

    message = MIMEText(text, 'html', 'utf-8')
    msgAlternative.attach(message)

    # send email
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_host_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, msgRoot.as_string())
        print(title + ' ' + name + ' success!')
    except smtplib.SMTPException:
        print(title + ' ' + name + ' fail!')
        return False
    return True


if __name__ == '__main__':
    # read reveivers info
    with open('test.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    error_list = []
    for line in lines:
        # split title, name, email
        words = line.strip().split('\t')
        assert len(words) == 3
        title = words[0].strip()
        name = words[1].strip()
        email = words[2].strip()
        # send an email
        flag = send_one(title, name, email)
        if not flag:
            error_list.append(line)
        sleep(1)
    if len(error_list) > 0:
        with open('error.txt', 'w') as f:
            for line in error_list:
                f.write(line)
