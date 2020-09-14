import socket

ip_port = ('127.0.0.1', 9999)
sk = socket.socket()          
sk.bind(ip_port)
print("-"*10)
print("[+] Setting Done!")
print("[+] Wating...")
sk.listen(5)
conn, address = sk.accept()
print("[+] Connect!")
print("[+] IP:",address[0])
print("[+] Port:",address[1])
print("[+] Type help for help.")
while True:
    data = input("Control "+address[0]+" :")
    if data == 'exit':
        conn.send(data.encode())
        print("[X] Connect Close")
        conn.close()
        break
    elif data == 'help':
        print("exit to quit")
    elif data != '':
        data = (data+" && echo [+] Command Request Done!")
        conn.send(data.encode())
        print(conn.recv(4096).decode('big5'))
    elif data == '':
        print("pls enter")
        continue
conn.close()
