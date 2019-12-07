"""
This file handles recieving of emails
"""
import email as mal
import imaplib

from bs4 import BeautifulSoup

import cleanexit
import lesssecureapps
import send_mails
import speech_ui


def get_first_text_block(msg):
    """
    This method recieves an email and returns the body
    """
    type = msg.get_content_maintype()
    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()

def get_email(host,port,email,password):
    """
    This method authenticates with imap to recieve emails
    """
    try :
        mail = imaplib.IMAP4_SSL(host,port)
    except:
        try:
            mail = imaplib.IMAP4_SSL(host,port)
        except:
            speech_ui.playsound("./data/connection-error.mp3")
            cleanexit.quit()
    
    try :
        mail.login(email,password)
    except:
        try:
            mail.login(email,password)
        except:
            text="I'm unable to login using the given credentials, Here are the credentials that am using. Email: %s . Password: %s"%(email,password)
            speech_ui.speak(text)
            speech_ui.playsound('./data/confirm-credentials.mp3')
            if(speech_ui.YesOrNo()):
                speech_ui.playsound('./data/ask-browser.mp3')
                browserapp=speech_ui.take_voice()
                lesssecureapps.browser(browserapp,email,password)
        else:
            cleanexit.quit()

    status,totalmail=mail.select(mailbox='inbox')
    del status
    text="You have A Total of %s, emails in your, inbox. Please wait as I search for unread emails"%str(totalmail).replace('b','')
    speech_ui.speak(text)
    status, data = mail.uid('search',None, "(UNSEEN)")
    inbox_item_list=data[0].split()
    try:
        new = int(inbox_item_list[-1])
        old = int(inbox_item_list[0])
    except IndexError:
        text="You have 0, unread emails . I am logging out . !Bye"
        speech_ui.speak(text)
        mail.close()
        mail.logout()
        cleanexit.quit()
   
    for i in range(new,old-1, -1):
        status, email_data = mail.uid('fetch',str(i).encode(), '(RFC822)' )
        raw_email = email_data[0][1].decode("utf-8")
        email_message = mal.message_from_string(raw_email)
        From=email_message['From']
        Subject=str(email_message['Subject'])
        if(Subject == ""):
            Subject="empty"
        text="You have a message from: %s . The subject Of the Email is: %s"%(From,Subject)
        speech_ui.speak(text)
        mail_message=get_first_text_block(email_message)
        usehtml="use a HTML compatible email viewer"
        if(mail_message.__contains__(usehtml)):
            for part in email_message.get_payload():
                if part.get_content_maintype() == 'text':
                    body=part.get_payload()
                    soup = BeautifulSoup(body, "html.parser")
                    txt = soup.get_text()
                    txt=txt.replace("To view the message, please use a HTML compatible email viewer!",'')
                    speech_ui.speak("The Body is: %s"%txt)
                    status, data = mail.store(str(i).encode(),'+FLAGS','\\Seen')
                    speech_ui.playsound('./data/ask-reply.mp3')
                    if(speech_ui.YesOrNo()):
                        send_mails.main(host,port,email,password,From)       
                    cleanexit.quit()
        else:
            text=mail_message
            speech_ui.speak("The Body is: %s"%text)
            speech_ui.playsound('./data/ask-reply.mp3')
            if(speech_ui.YesOrNo()):
                send_mails.main(host,port,email,password,From)
            status, data = mail.store(str(i).encode(),'+FLAGS','\\Seen')
            cleanexit.quit()
