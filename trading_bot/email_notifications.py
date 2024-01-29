import smtplib
from email.message import EmailMessage

def send_email(ticker, side, price):
    msg = EmailMessage()
    msg.set_content(ticker + ' is ' + side + ' at %4.3f' %price)
    #msg.set_content('blabla')

    msg['Subject'] = 'Bot Alert'
    msg['From'] = "botalert06@gmail.com"
    msg['To'] = "jakob.kamnik@gmail.com"
    #msg['To'] = "botalert06@gmail.com"



    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('botalert06@gmail.com', 'mwzxgphdehxocevj')


    #https://www.letscodemore.com/blog/smtplib-smtpauthenticationerror-username-and-password-not-accepted/
    # server.sendmail('jakob.kamnik@gmail.com', #from
    #                 'a.jakob.kamnik@gmail.com', #to
    #                 'Subject: Bot',
    #                 'blablabalba') #message
    server.send_message(msg)
    server.quit()

#send_email('hbar', 'sell', 0.20)


#-------------------------------------------------------------------------------------------------

#whatsapps? 
