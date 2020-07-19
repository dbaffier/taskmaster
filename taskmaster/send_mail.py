# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    send_mail.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/17 11:20:23 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/15 16:29:49 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
import smtplib
import threading
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def start_reporter(name_prog):
    t = threading.Thread(target=reporter, args=(name_prog, None))
    t.start()

def start_manual_reporter(name_prog):
    t = threading.Thread(target=manual_reporter, args=(name_prog, None))
    t.start()

def reporter(name, null):
    you = "dbaffier@student.42.fr"
    me = "taskmaster_rep@hotmail.com"

    now = time.strftime("%c")
    msg = MIMEMultipart()
    # msg = MIMEText(str(now) + ', program "' + name + '" crashed !')

    msg['Subject'] = '[CRASH] Program [' + name  + '] crashed !'
    msg['From'] = me
    msg['To'] = you
    password = "answer42"

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except Exception as e:
        server = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

    try:
        server.connect("smtp-mail.outlook.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(me, password)
        server.sendmail(me, you, msg.as_string())
        server.quit()
    except Exception as e:
        pass