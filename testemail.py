import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg["subject"] = to

    user = "test@gmail"
    password = "App password"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.quit()

#testing the file
if __name__ == '__main__':
    email_alert("Test email","Texting for test purposes","test@gmail")
