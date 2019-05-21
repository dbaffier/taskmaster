import time
import smtplib
from email.mime.text import MIMEText


def reporter(name, null):
    print("Enter reported")
 #   me = 'taskmaster@42.fr'
    me = 'meiline.monier@yahoo.fr'
    you = 'dorianbaffier@hotmail.fr'
 #   you = 'dbaffier@student.42.fr'

    now = time.strftime("%c")
    msg = MIMEText(str(now) + ', program "' + name + '" crashed !')

    msg['Subject'] = '[CRASH] Program [' + name  + '] crashed !'
    msg['From'] = me
    msg['To'] = you
    

    try:
        s = smtplib.SMTP('smtp.live.com')
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_passwd)
        s.sendmail(me, you, "Hello")
 #       s.send_message(msg)
        s.quit()
    except:
        print("Pass")
        pass
    print("out")

if __name__ == '__main__':
    reporter("hello", None)

