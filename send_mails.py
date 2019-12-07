import base64
import email
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror
from time import sleep

import yagmail

import cleanexit
import file_handler
import speech_ui
import lesssecureapps


def connection(host,port):
    """
    This function connects to the mail service
    and returns a connection instance
    """
    try:
        mail = smtplib.SMTP(host,port)
    except gaierror:
        speech_ui.playsound('./data/connection-error.mp3')
        cleanexit.quit()
    except (ConnectionRefusedError,smtplib.SMTPConnectError) as e:
        speech_ui.playsound('./data/bug.mp3')
        if(speech_ui.YesOrNo):
            bug=e+" "+host+" "+port
            print(bug)
        cleanexit.quit()

    return mail
def login(host,port,email,password):
    """
    Check login from user
    """
    try:
        mail=connection(host,port)
        #Hostname to send for this command defaults to the FQDN of the local host.
        mail.ehlo()
        #Start a secure connection
        mail.starttls()
        #attempt login
        mail.login(email,password)
    except smtplib.SMTPAuthenticationError:
        text="I'm unable to login using the given credentials, Here are the credentials that am using. Email: %s . Password: %s"%(email,password)
        speech_ui.speak(text)
        speech_ui.playsound('./data/confirm-credentials.mp3')
        if(speech_ui.YesOrNo()):
            speech_ui.playsound('./data/ask-browser.mp3')
            browserapp=speech_ui.take_voice()
            lesssecureapps.browser(browserapp,email,password)
        else:
            cleanexit.quit()
def gmail_send(sender,receiver,password):
    """
    Interact with gmail api to send mails
    """
    yag = yagmail.SMTP(user=sender,password=password)
    speech_ui.playsound("./data/ask-subject.mp3")
    subject=speech_ui.take_voice()
    if(subject=="null"or subject=="empty"):
         subject=""
    speech_ui.playsound("./data/ask-contents.mp3")
    body = speech_ui.take_voice()
    while True:
        if(speech_ui.confirm(body)):
            break
        else:
            continue
    speech_ui.playsound("./data/ask-attachment.mp3")
    if(speech_ui.YesOrNo()):
        speech_ui.playsound("./data/ask-file.mp3")
        filename=speech_ui.take_voice()
        filename=file_handler.search_file(filename)
        if(filename==""):
            speech_ui.playsound('./data/send-blank.mp3')
            if(speech_ui.YesOrNo()):
                yag.send(to=receiver,subject=subject,contents=body)
            else:
                cleanexit.quit()
        else:
            yag.send(to=receiver,subject=subject,contents=body,attachments=filename)
    speech_ui.playsound("./data/email_sent.mp3")

def compose_mail(sender,reciever):
    """
    This method composes the email with acceptable standards
    and retunrns as a message string
    """
    sender_email = sender
    receiver_email = reciever
    speech_ui.playsound("./data/ask-subject.mp3")
    subject = speech_ui.take_voice()
    if(subject=="null" or subject =="empty"):
         subject=""
    speech_ui.playsound("./data/ask-contents.mp3")
    body = speech_ui.take_voice()
    while True:
        if(speech_ui.confirm(body)):
            break
        else:
            continue
    #Ask if attachment is needed
    speech_ui.playsound("./data/ask-attachment.mp3")
    if(speech_ui.YesOrNo()):
        #Ask name of attchments
        speech_ui.playsound('./data/ask-file.mp3')
        filename=speech_ui.take_voice()
        filename=file_handler.search_file(filename)
        if(filename==""):
            speech_ui.playsound('./data/send-blank.mp3')
            if(speech_ui.YesOrNo()):
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = receiver_email
                text=msg.as_string()
            else:
                cleanexit.quit()
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        # Add body to email
        message.attach(MIMEText(body, "plain"))
        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
    else:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        text=msg.as_string()
    return text

def main(host,port,sender_email,sender_password,reciever_email):
    try:
        mail=connection(host,port)
        #Hostname to send for this command defaults to the FQDN of the local host.
        mail.ehlo()
        #Start a secure connection
        mail.starttls()
        #attempt login
        mail.login(sender_email,sender_password)

    except smtplib.SMTPAuthenticationError:
        text="I'm unable to login using the given credentials, Here are the credentials that am using. Email: %s . Password: %s"%(sender_email,sender_password)
        speech_ui.speak(text)
        speech_ui.playsound('./data/confirm-credentials.mp3')
        if(speech_ui.YesOrNo()):
            speech_ui.playsound('./data/ask-browser.mp3')
            browserapp=speech_ui.take_voice()
            lesssecureapps.browser(browserapp,sender_email,sender_password)
        else:
            cleanexit.quit()
    if(host=="gmail"):
        gmail_send(sender_email,reciever_email,sender_password)
        speech_ui.playsound("./data/email_sent.mp3")
        cleanexit.quit()

    else:
        message=compose_mail(sender_email,reciever_email)
        mail.sendmail(sender_email,reciever_email,message)
        speech_ui.playsound("./data/email_sent.mp3")
        cleanexit.quit()