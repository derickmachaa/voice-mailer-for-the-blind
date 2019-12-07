import speech_recognition as sr
from playsound import playsound
import random
import string
import http
import cleanexit
from gtts import gTTS

def speak(txt):
    """
    This method recieves a text and turns it into audio and then plays it
    """
    try:
        audio=gTTS(text=txt,lang='en-US')
        savelocation="./tmp/"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(9)])+".mp3"
        #save audio
        audio.save(savelocation)
        playsound(savelocation)
    except:
        playsound("./data/connection-error.mp3")
        cleanexit.quit()
    

def take_voice():
    """
    This method takes in voice from user microphone and decodes it and turns it to text 
    then returns the text
    """
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        playsound("./data/prompt.mp3")
        audio=r.listen(source)
    playsound("./data/interpreting.mp3")
    #Convert audio to text
    try:
        text=r.recognize_google(audio)
        if(text=="nevermind" or text == "exit"):
            cleanexit.quit()
    except sr.UnknownValueError:
        playsound("./data/didnt_understand.mp3")
        text=take_voice()
    except (sr.RequestError,http.client.RemoteDisconnected):
        playsound("./data/connection-error.mp3")
        cleanexit.quit()
    return text

def confirm(text):
    """
    This method asks a questions and returns true if answer is yes
    and false if answer is no
    """
    speak("This is what i Understood,: %s. "%text)
    playsound('./data/correct.mp3')
    ListOfStrings=['yes','yeah','yeh','ofcourse']
    text=take_voice()
    if(text in ListOfStrings):
        return True
    else:
        return False

def YesOrNo():
    """
    This method asks a yes or no question and returns  true if answer is yes
    and false if answer is no
    """
    ListOfYesStrings=['yes','yeah','yeh','ofcourse','obvious','true']
    ListOfNoStrings=['no','nah']
    text=take_voice()
    if(text in ListOfYesStrings):
        return True
    elif(text in ListOfNoStrings):
        return False