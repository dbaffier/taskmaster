# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    send_mail.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/17 11:20:23 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/21 15:53:19 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
import smtplib
import threading

from email.mime.text import MIMEText

def start_reporter(name_prog):
    t = threading.Thread(target=reporter, args=(name_prog, None))
    t.start()

def start_manual_reporter(name_prog):
    t = threading.Thread(target=manual_reporter, args=(name_prog, None))
    t.start()

def reporter(name, null):
    print("Enter reported")
 #   me = 'taskmaster@42.fr'
    you = 'meiline.monier@yahoo.fr'
    me = 'dorianbaffier@hotmail.fr'
 #   you = 'dbaffier@student.42.fr'

    now = time.strftime("%c")
    msg = MIMEText(str(now) + ', program "' + name + '" crashed !')

    msg['Subject'] = '[CRASH] Program [' + name  + '] crashed !'
    msg['From'] = me
    msg['To'] = you

    try:
        s = smtplib.SMTP('smtp.live.com')
        s.sendmail(me, you, msg.as_string())
 #       s.send_message(msg)
        s.quit()
    except:
        print("Pass")
        pass
    print("out")
