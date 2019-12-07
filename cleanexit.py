import os
import sys
import speech_ui

def quit():
    """
    This method provides a clean exit clearing all the temporary files
    """
    speech_ui.playsound('./data/exit.mp3')
    os.system("rm ./tmp/*")
    sys.exit()