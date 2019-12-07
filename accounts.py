import sqlite3
import speech_ui

#create a connection to a local database file
conn=sqlite3.connect("./data/accounts.db")
cursor=conn.cursor()

def create_tables():
    """
    This method creates a user and email tables in sqlite3 database
    """
    sql="""
    CREATE TABLE IF NOT EXISTS `User`(
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT NOT NULL UNIQUE,
	`Gender`	TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS `Hosts` (
	`Host_Name`	TEXT NOT NULL,
	`IMAP_NAME`	TEXT NOT NULL,
	`IMAP_PORT`	NUMERIC NOT NULL,
	`SMTP_NAME`	TEXT NOT NULL,
	`SMTP_PORT`	NUMERIC NOT NULL,
	PRIMARY KEY(`Host_Name`)
    );
    CREATE TABLE IF NOT EXISTS `Accounts` (
	`Email_AC`	TEXT NOT NULL,
	`Email_Pass`	TEXT NOT NULL,
	`Host_Name`	TEXT NOT NULL,
	`ID`	INTEGER NOT NULL,
	FOREIGN KEY(`ID`) REFERENCES `User`(`ID`),
	PRIMARY KEY(`Email_AC`),
	FOREIGN KEY(`Host_Name`) REFERENCES `Hosts`(`Host_Name`)
    )
    """
    cursor.executescript(sql)
    conn.commit()

def get_accounts(user_id):
    """
    This method recieves user_id and returns the emails accounts from the database
    """ 
    sql="select Email_AC,Email_Pass,Host_Name FROM Accounts where ID=%s"%user_id
    rows=cursor.execute(sql)
    details=rows.fetchall()
    return details

def get_logins(email):
    """
    recieve an email and returns the login credentials
    """
    sql="SELECT Email_AC,Email_Pass,Host_Name FROM Accounts WHERE Email_AC='%s'"%email
    row=cursor.execute(sql).fetchone()
    return row

def insert_user(name,gender):
    """
    This method inserts  a new user into the database
    """
    sql="INSERT INTO User (Name,Gender) VALUES('%s','%s')"%(name,gender)
    try:
        cursor.execute(sql)
    except sqlite3.IntegrityError:
        speech_ui.speak("User %s already exists please try with a another username")
    conn.commit()

def get_host(host_name):
    """
    Recieve a host name and returns the port and hostname of the emailservice
    """
    sql="SELECT IMAP_NAME,IMAP_PORT,SMTP_NAME,SMTP_PORT FROM Hosts where Host_Name='%s'"%host_name
    row=cursor.execute(sql).fetchone()
    return row

def add_account(host,user_id,email,password):
    """
    This method inserts a new email account and password to the database
    """
    sql="insert into Accounts Values('%s','%s','%s','%s')"%(email,password,host,user_id)
    try:
        cursor.execute(sql)
    except:
        speech_ui.speak("Email address already exists try with a new one")
    conn.commit()

def delete_account(email):
    """
    This method deletes an email from the known  email accounts
    """
    sql="DELETE FROM Accounts WHERE Email_AC='%s'"%email
    cursor.execute(sql)
    conn.commit()

def delete_user(name):
    """
    Delete a user in the database
    """
    sql="DELETE FROM User WHERE Name='%s'"%name
    cursor.execute(sql)
    conn.commit()

def get_id(name):
    sql="SELECT ID from User WHERE Name='%s'"%name
    row=cursor.execute(sql).fetchone()
    for i in row:
        ID=i
    return ID

def check_users_in_db():
    """
    Check if db is empty or not..if contains user return a tuple with True and rows
    else return False with empty row
    """
    sql="select * from User"
    rows=cursor.execute(sql).fetchall()
    if rows:
        return (True,rows)
    else:
        return (False,rows)
create_tables()