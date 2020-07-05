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
    msg = MIMEText(str(now) + ', program "' + name + '" crashed !')

    msg['Subject'] = '[CRASH] Program [' + name  + '] crashed !'
    msg['From'] = me
    msg['To'] = you
    password = "answer42"

    context=ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.live.com", 587) as s:
            s.ehlo()
            s.starttls(context=context)
            s.ehlo()
            s.login(me, password)
            try:
               s.sendmail(me, you, msg.as_string())
            except:
                print("Send mail fail")
                pass
            s.quit()
    except:
        pass
