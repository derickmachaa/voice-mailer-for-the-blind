import tarfile
import zipfile

import accounts
import cleanexit
import recieve_mails
import send_mails
import speech_ui


def get_host(email):
    """
    This method recieves an email splits it and returns the email host
    """
    host=email.split('@').__getitem__(1).split('.').__getitem__(0)
    return host

def get_name():
    """Ask for username 
    """
    speech_ui.playsound('./data/ask-name.mp3')
    text=speech_ui.take_voice()
    name=text.replace(' ','')
    while True:
        if (speech_ui.confirm(name)):
            break
        else:
            continue
    return name

def get_email():
    """Ask for email
    """
    speech_ui.playsound('./data/ask-email.mp3')
    text=speech_ui.take_voice()
    e_mail=text.replace('at','@').replace(' ','').replace('dot','.')
    while True:
        if (speech_ui.confirm(e_mail)):
            break
        else:
            continue
    return e_mail

def get_dest_email():
    """Ask for email
    """
    speech_ui.playsound('./data/ask-destmail.mp3')
    text=speech_ui.take_voice()
    e_mail=text.replace('at','@').replace(' ','').replace('dot','.')
    while True:
        if (speech_ui.confirm(e_mail)):
            break
        else:
            continue
    return e_mail

def get_password():
    """Ask for password
    """
    speech_ui.playsound('./data/ask-password.mp3')
    text=speech_ui.take_voice()
    password=text.replace(' ','')
    while True:
        if (speech_ui.confirm(password)):
            break
        else:
            continue
    return password

def get_gender():
    """
    Ask for gender
    """
    speech_ui.playsound('./data/ask-gender.mp3')
    text=speech_ui.take_voice()
    if(text=="mail"):
        text="male"
    return text

def check_login(email,password):
    host=get_host(email)
    imap_name,imap_port,smtp_name,smtp_port=accounts.get_host(host)
    del imap_name,imap_port
    if(send_mails.login(smtp_name,smtp_port,email,password)):
        return True
    else:
        return False        

def initial_setup():
    ##This is the first installation setup
    #extract executables needed 
    tfile=tarfile.open('./bin/geckodriver-linux64.tar.gz')
    tfile.extractall(path='./bin')
    zfile=zipfile.ZipFile('./bin/chromedriver_linux64.zip')
    zfile.extractall(path='./bin')
    speech_ui.playsound("./data/intro.mp3")
    name=get_name()    
    gender=get_gender()
    accounts.insert_user(name,gender)
    emailaddress=get_email()
    password=get_password()
    #check if login is true and insert to db
    if(check_login(emailaddress,password)):
        host=get_host(emailaddress)
        accounts.add_account(host,accounts.get_id(name),emailaddress,password)
    speech_ui.playsound('./data/after-intro.mp3')
    speech_ui.playsound('./data/quit.mp3')
    main()
def main():
    """The main controller
    """
    NotEmpty,Users=accounts.check_users_in_db()
    if (NotEmpty):
        numberofusers=len(Users)
        if(numberofusers>1):
            speech_ui.playsound('./data/multiple-users.mp3')
            text=get_name()
            try:
                ID=accounts.get_id(text)
                username=text
                acc=accounts.get_accounts(ID)
            except (UnboundLocalError,TypeError):
                speech_ui.playsound('./data/no-user.mp3')
                cleanexit.quit()
            if(len(acc)>1):
                try:
                    email_acc=get_email()
                    emailacc,password,host=accounts.get_logins(email_acc)
                except (TypeError,UnboundLocalError):
                    speech_ui.playsound('./data/no-email.mp3')
                    cleanexit.quit()
            else:
                if not acc:
                    speech_ui.speak("%s! You do not have an account Please add one"%username)
                    newemail=get_email()
                    newhost=get_host(newemail)
                    newpassword=get_password()
                    accounts.add_account(newhost,ID,newemail,newpassword)
                    cleanexit.quit()
                else:
                    for i in acc:
                        emailacc,password,host=i
        else:
            for i in Users:
                ID,username,gender=i
            acc=accounts.get_accounts(ID)
            if(len(acc)>1):
                try:
                    speech_ui.playsound('./data/many-emails.mp3')
                    email_acc=get_email()
                    emailacc,password,host=accounts.get_logins(email_acc)
                except (TypeError,UnboundLocalError):
                    speech_ui.playsound('./data/no-email.mp3')
                    cleanexit.quit()
            else:
                if not acc:
                    speech_ui.speak("%s! You do not have an account Please add one"%username)
                    newemail=get_email()
                    newhost=get_host(newemail)
                    newpassword=get_password()
                    accounts.add_account(newhost,ID,newemail,newpassword)
                    cleanexit.quit()
                else:
                    for i in acc:
                        emailacc,password,host=i
        host=get_host(emailacc)
        imapname,imapport,smtpname,smtpport=accounts.get_host(host)
        text="""
        Welcome %s!. What would you wish to do?
        1. Check inbox.
        2. Compose email.
        3. Add an account.
        4. Delete an account.
        5. Add a new user.
        6. Delete a user."""%username
        speech_ui.speak(text)
        text=speech_ui.take_voice()
        homophonesOne=['one','1','warn']
        homophonesTwo=['two','2','too']
        homophonesFour=['for','4']
        if(text in homophonesOne):
            recieve_mails.get_email(imapname,imapport,emailacc,password)
        elif(text in homophonesTwo):
            reciever=get_dest_email()
            send_mails.main(smtpname,smtpport,emailacc,password,reciever)
        elif(text=='3'):
            newemail=get_email()
            newhost=get_host(newemail)
            newpassword=get_password()
            accounts.add_account(newhost,ID,newemail,newpassword)
            cleanexit.quit()
        elif(text in homophonesFour):
            text=get_email()
            accounts.delete_account(text)
            cleanexit.quit()
        elif(text=='5'):
            name=get_name()
            gender=get_gender()
            accounts.insert_user(name,gender)
            cleanexit.quit()
        elif(text=='6'):
            name=get_name()
            accounts.delete_user(name)
            cleanexit.quit()
    else:
        initial_setup()

if __name__ == "__main__":
    main()
