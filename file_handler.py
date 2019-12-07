import subprocess
import speech_ui

def search_file(name):
    """This method searchs a file name and returns a list of available files
    finds the exact file and returns full path
    """
    #find in current user directory
    filenames=subprocess.getoutput("find ~ -iname *%s* " %name)
    if(filenames==""):
        #find in usb and mounted spaces
        filenames=subprocess.getoutput("find /media -iname *%s* " %name)
        if(filenames==""):
            filenames=subprocess.getoutput("find /mnt -iname *%s* " %name)
            if(filenames==""):
                filenames=subprocess.getoutput("find / -iname *%s* " %name)
                if(filenames==""):
                    speech_ui.playsound('./data/ask-filename-again.mp3')
                    if(speech_ui.YesOrNo()):
                        name=speech_ui.playsound('./data/ask-file.mp3')
                        search_file(name)
                    else:
                        filename=""
    arrays=filenames.splitlines()
    length=len(arrays)
    number=0
    if(length>1):
        speech_ui.speak("i found %s mathcing files"%length)
        speech_ui.playsound("./data/file-prompt.mp3")
        for i in arrays:
            filename=i
            text="file "+number+" path is: "+filename.replace('/',', ')
            speech_ui.speak(text)
            number+=1
        speech_ui.playsound('./data/ask-number.mp3')
        num=int(speech_ui.take_voice())
        filename=arrays.__getitem__(num)
    elif(length<=1):
        for i in arrays:
            filename=i
            speech_ui.speak("file located is :%s. Is this the correct file?"%filename.replace('/',', '))
            if not (speech_ui.YesOrNo()):
                filename=""
    return filename
