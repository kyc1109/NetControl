#!/usr/bin/python3
#coding=utf8
import sys, os, ctypes, threading
#被控端
def getInfo():
    from uuid import getnode as get_mac
    import uuid, platform
    global host, ip, getMAC
    host=platform.node()
    ip=socket.gethostbyname(socket.getfqdn())
    try:
        mac = get_mac() #there's no way to determine which MAC it returned as 48 bit integer.
        getMAC = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))  #XX:XX:XX:XX:XX:XX
        #print(':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2)))
    except:
        getMAC="00:00:00:00:00:00"

    print("Host:",host)
    print("IP:",ip)
    print("MAC:",getMAC)
    getUUID=uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    print("UUID:",uuid.NAMESPACE_DNS)
    return getMAC




#1. 參考一下網路聊天室的作法
#2. 把Rx, Tx的多執行緒用while包起來
import socket, os, sys, time, subprocess        # Import socket module
from subprocess import Popen, PIPE
from importlib import reload
reload(sys)

#0==================================       #http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
port = 80808                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

def get_conn():
    #show here
    print('SUT listening...')
    getInfo()
    #1==================================
    while True: #Loop for listening

    #2==================================
        try:
            conn, addr = s.accept()     # Establish connection with client.
            print('Get connection from', addr) #get conn from server
            #Hello=conn.recv(1024).decode("utf-8")
            #print('SUT received:', Hello) #R0 Hello server!, repr() like as str()

            while conn:
                sys.path.append(os.getenv('USERPROFILE'))
                sys.path.append((os.getenv('USERPROFILE')+"\\Desktop") )
                os.chdir((os.getenv('USERPROFILE')+"\\Desktop")) #change current dir from system32 to Desktop

                data = conn.recv(1024)  #R1, 4096 is recommand
                if not data:
                    pass
                elif data.decode("utf-8").lower()=="__scan_uut__": #scan all of UUT
                    global host, ip, getMAC
                    UUT_iInfo=(host+","+getMAC+","+ip)
                    send_data2=UUT_iInfo
                    print(UUT_iInfo)
                    conn.sendall(send_data2.encode('utf-8'))
                    conn.close()
                elif  data.decode("utf-8").lower()=="r" or data.decode("utf-8").lower()=="remove":
                    remove()
                    conn.close()
                #run cmd with data.decode("utf-8")
                else:
                    tt = threading.Thread(target=taskThread,args=(data.decode("utf-8"),))
                    tt.start() 
                    conn.close()
        except IOError as e:
            #pass
            print("I/O error({0}): {1}".format(e.errno, e.strerror)) #0307 error code 10038
        except socket.error as msg:
            print("Socket Error: %s" % msg)
        except TypeError as msg:
            print("Type Error: %s" % msg)
        except:
            print("unknown error")
        finally: 
            #print('Successfully !')
            #print('Sending finished')
            #conn.send('Thank you for connecting\n')
            conn.close()
            get_conn()
            #print '\n\n\n Exit for error. Try to reopen' #fail 2
#            get_conn() #re-listening
            #os.system("pause")
def taskThread(cmd_str):
    global cmd_previous 
    if cmd_previous == cmd_str:
        print("The cmd is the same, ignore it.")
        cmd_str="echo The cmd is the same, ignore it."
    else:
        cmd_previous = cmd_str
    p=subprocess.Popen(cmd_str,shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    stdout,stderr =p.communicate()

    data_str = cmd_str
    #Do stderr later                 
    send_data = str("\nSUT got msg: \n===========START================\n"+
                "cmd: "+ data_str +"\n"+
                "stdout: \n"+stdout.decode("utf-8","ignore")+"\n"+
                #"stderr: \n"+stderr+"\n"+
                "\n===========END================\n")
    
    send_data2="OK, just do it." #to control
    print("sendall")
    try: #ack to Controller
        print("result... "+send_data)
    except:
        print("I/O error(10035)")
def auto_run():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    filename=filename.replace(".py", ".exe")
    filefullpathname=dirname+"\\"+filename
    regkey="HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    print("filename:",filename)
    os.chdir(os.environ['USERPROFILE']) # to find file itself
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if file == filename:
                os.chdir(root)
                filefullpathname=os.path.abspath(os.path.join(root,file))
                print(filefullpathname)
    try:
        os.system("reg add "+regkey+" /v stress_"+filename.replace(".exe","")+" /t REG_SZ /d "+filefullpathname+" /f")
        print("auto run add ok")
        #os.system("timeout /t 10")
    except:
        print("auto run reg failed !!!")
        os.system("timeout /t 30")
    try:
        #remove auto run if argv1 is remove
        if sys.argv[1].lower()=="remove":
            remove()
            sys.exit(0)
    except:
        pass
def remove():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    filenameExe = filename.replace(".py", ".exe") #.py to .exe
    regkey="HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    os.system("reg delete "+regkey+" /v stress_"+filenameExe.replace(".exe","")+" /f") #original name is .py    

    filenameini = filename.replace(".py", ".ini") #Ethan_U.ini
    if os.path.exists(filenameini):
        os.system("del /q "+filenameini)

    ini = os.environ['SYSTEMROOT']+"\\system32\\"+filenameini
    if os.path.exists(ini):
        os.system("del /q "+ini)

def first_run_check():
    #Bug permission denied 
    dirname, filename = os.path.split(os.path.abspath(__file__))
    filename=filename.replace(".py", ".ini") #Ethan_U.ini
    try:
        if os.path.exists(filename):
            if len(sys.argv)>1:
                if sys.argv[1].lower()=="remove":
                    remove()
        else:
            wLog=open(filename, "w")
            wLog.write(filename)
            wLog.close()
            #os.system("attrib +h "+filename) #for hidden
            auto_run()
    except IOError as e:
            #pass
        print("I/O error({0}): {1}".format(e.errno, e.strerror)) #0307 error code 10038
    except socket.error as msg:
        print("Socket Error: %s" % msg)
    except TypeError as msg:
            print("Type Error: %s" % msg)
    except:
        print("can not catch error")
    finally: #debug for permission denied
        pass


def is_admin(): #https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
        #os.chdir(os.path.join(os.getenv("USERPROFILE")+"\\Desktop"))
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1) #for py 3
            #ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1) #for py2
            print("Not admin")
            os.system("timeout /t 1")
            return False

if __name__ == "__main__":  # Start from here
    os.system('mode con: cols=50 lines=6') #set cmd window size
    #auto_run()
    cmd_previous=""
    if is_admin():  #check is admin or not
        first_run_check() 
        while True:
            get_conn()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
