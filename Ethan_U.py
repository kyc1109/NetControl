#!/usr/bin/python3
#coding=utf8
#sys.setdefaultencoding('utf8')
import sys, os


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
    print("MAC",getMAC)
    getUUID=uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    print("UUID:",uuid.NAMESPACE_DNS)
    return getMAC




#1. 參考一下網路聊天室的作法
#2. 把Rx, Tx的多執行緒用while包起來
import socket, os, sys, time, subprocess        # Import socket module
from subprocess import Popen, PIPE
from importlib import reload
reload(sys)

#0==================================                                #http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
port = 60001                    # Reserve a port for your service.
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
            print('SUT received', conn.recv(1024).decode("utf-8")) #R0 Hello server!, repr() like as str()

            while conn:
                data = conn.recv(1024)  #R1, 4096 is recommand
                if not data:
                    pass
                elif data.decode("utf-8").lower()=="a": #scan all of UUT
                    global host, ip, getMAC
                    UUT_iInfo=[host,ip,getMAC]
                    send_data2=" ".join(UUT_iInfo)
                    print(" ".join(UUT_iInfo))
                    conn.sendall(send_data2.encode('utf-8'))
                    conn.close()
                elif data.decode("utf-8").lower()=="r":
                    dirname, filename = os.path.split(os.path.abspath(__file__))
                    filename=filename.replace(".py", ".exe")
                    filefullpathname=dirname+"\\"+filename
                    regkey="HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                    os.system("reg delete "+regkey+" /v stress_"+filename.replace(".exe","")+" /f")
                    conn.close()
                    
                else:
                    print("Receiving...: "+data.decode("utf-8")) #get data from control side
                    #conn.sendall("Roger that.".encode('utf-8'))

                    #execute controller's cmd
                    p=subprocess.Popen(data.decode("utf-8"),shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
                    stdout,stderr =p.communicate()
                    print("type stderr",type(stdout))  #stdout is bytes              
                    print("type stderr",type(stderr))    
                    
                    #print("send_data")
                    data_str = data.decode("utf-8","ignore")

                    #Do stderr later                 
                    send_data = str("\nSUT got msg: \n===========START================\n"+
                                "cmd: "+ data_str +"\n"+
                                "stdout: \n"+stdout.decode("utf-8","ignore")+"\n"+
                                #"stderr: \n"+stderr+"\n"+
                                "\n===========END================\n")
                    
                    send_data2="OK, just do it." #to control
                    print("sendall")
                    try: #ack to Controller
                        conn.sendall(send_data2.encode('utf-8')) #S1, buffer不足
                        #while (send_data):
                        #    conn.send(send_data)
                        print("result... "+send_data)
                    except:
                        print("I/O error(10035)")


                    print("\nSUT listening... ") #End of cmd...
                    #getInfo()
                    conn.close()
        except IOError as e:
            pass
            #print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except socket.error as msg:
            print("Socket Error: %s" % msg)
        except TypeError as msg:
            print("Type Error: %s" % msg)
        finally: 
            #print('Successfully !')
            #print('Sending finished')
            #conn.send('Thank you for connecting\n')
            conn.close()
            get_conn()
            #print '\n\n\n Exit for error. Try to reopen' #fail 2
#            get_conn() #re-listening
            #os.system("pause")
def auto_run(): #bug auto run twice the place will be wrong, walk to solved it.
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
                #print(os.path.abspath(os.path.join(file)))
                filefullpathname=os.path.abspath(os.path.join(root,file))
                print(filefullpathname)
    try:
        #print("regkey: ","reg add "+regkey+" /v stress_"+filename.replace(".exe","")+" /t REG_SZ /d "+filefullpathname+" /f")
        os.system("reg add "+regkey+" /v stress_"+filename.replace(".exe","")+" /t REG_SZ /d "+filefullpathname+" /f")
        print("auto run add ok")
        #os.system("timeout /t 10")

    except:
        print("auto run reg failed !!!")
        os.system("timeout /t 30")

    try:
        #remove auto run if argv1 is remove
        if sys.argv[1].lower()=="remove":
            regkey="HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            os.system("reg delete "+regkey+" /v stress_"+filename.replace(".exe","")+" /f")
            print("auto run remove ok")
            sys.exit(0)
    except:
        pass

if __name__ == "__main__":  # Start from here
    os.system('mode con: cols=50 lines=6') #set cmd window size
    auto_run()
    while True:
        get_conn()

"""
Know issue buffer not ready 如果傳太多data會lose data
Bug, 1. 對反應比較久或比較多資料的會斷線
    eg 1. I/O error(10035): 無法立即完成通訊端操作，而且無法停止。
    eg 2. delLog.exe
    eg 3. FFXV install

"""
