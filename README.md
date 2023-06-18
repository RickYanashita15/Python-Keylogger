# Python-Keylogger
An advanced Python keylogger for macOS (local use). This Python keylogger will be able to log keystrokes, mouse clicks, system information, screenshot, audio via the microphone, and a photo via the front-facing camera. 
**This program is for educational and testing purposes only. Do not use it maliciously. I am not promoting or encouraging any illegal activities.**

## Project Description
This keylogger project was inspired by and adapted from cyberacademy.org & Grant Collins’s “Create an Advanced Keylogger in Python - Crash Course” video on Youtube. Although most of the ideas and code are from these resources, the project crash course video was done for a keylogger compatible with a Windows system and thus I had to modify my implementation to work on a macOS system. Some parts of the code had to be tweaked slightly, some functions had to be entirely new implementations, and many different modules were used to collect information from a macOS system (unlike the modules for a Windows keylogger). 

Some notable changes I made were that I added more detail to the email description (like the date/time of the log) and information on what exactly each file is. This would allow anyone using this keylogger to understand the contents of the email. Additionally, I created a whole new implementation to collect camera data (as a photo). I believe a function like this would prove useful if the keylogger was to be used to determine who uses the device. 

The keylogger has five functions for collecting information: a regular keylogger, a function that collects device/system information, a function that copies text from the system’s clipboard, a function that collects audio, a function that takes a screenshot, and a function that takes a photo from the front-facing camera. The microphone runs for 10 seconds and the regular keylogger runs for 1 minute (times can be modified but were kept short for the sake of testing and debugging). Overall, it takes around two minutes to collect all this information, and in the end, all the information is sent via SMTP to a Gmail address. 

Through implementing this project, I learned how to:
- Allow/Disallow VSCode and iTerm (my terminal) to get access to the system’s microphone and cameras
- Write to files, in Python
- Use a Listener with on_press and on_release arguments
- Add timers to Python functions
- Access system/device information through Python
- Send an email to a Gmail address using Python and the SMTP server 587
- Mess with macOS & Gmail security settings

## Some Images of the keylog email and individual file contents

The keylog email with description and attachments:
<img width="1440" alt="Screenshot 2023-06-17 at 3 48 39 PM" src="https://github.com/RickYanashita15/Python-Keylogger/assets/65827502/7cf205ba-a61e-4a86-bfd5-abcc18cfdb85">

The actual key_log.txt file: 
<img width="869" alt="Screenshot 2023-06-17 at 3 49 36 PM" src="https://github.com/RickYanashita15/Python-Keylogger/assets/65827502/00b8995e-b6ea-4031-b769-d8a5debb418c">

The system_information.txt file:
<img width="1133" alt="Screenshot 2023-06-17 at 3 49 57 PM" src="https://github.com/RickYanashita15/Python-Keylogger/assets/65827502/70523c4d-88d0-4aeb-8d26-ab6f214c5e09">

The clipboard_information.txt file: 
<img width="1134" alt="Screenshot 2023-06-17 at 3 50 19 PM" src="https://github.com/RickYanashita15/Python-Keylogger/assets/65827502/4ddf4ff0-a662-4c32-b003-f0b0bdb1aeeb">





