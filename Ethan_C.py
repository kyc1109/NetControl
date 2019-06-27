#!/usr/bin/python3
#coding=utf8

#主控端, 需求:能遠端執行命令或資料夾
import socket, os, sys, time, datetime, threading         # Import socket module
from subprocess import Popen   #http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
from importlib import reload
reload(sys)

def get_control(UUT_IP, UUT_cmd): #no response
    try:
        #0==================================
        port = 80808      
        s = socket.socket()             # Create a socket object
        host = socket.gethostname()     # Get local machine name
        #print("H:Controller IP:",socket.gethostbyname(socket.getfqdn()))  # Reserve a port for your service.
        UUT_Return=""
        #1==================================
        #server="10.110.141.66"
        #print("H:UUT/Remote IP:",UUT_IP)
        s.settimeout(1)
        s.connect((UUT_IP, port))    #s.connect((host, port)) 
        s.settimeout(5)
        #2==================================
        remote_cmd_str = UUT_cmd # str(input("\nplease input the cmd (default is help): \n") or "help")
        remote_cmd = remote_cmd_str.encode('utf-8')
        if not remote_cmd.lower():    #for receive others data
            print("Do nothing")
        else:
            s.send(remote_cmd)   #S1
        s.close()

    except socket.timeout as msg:
        #print("Socket Error: %s" % msg)
        print("%s is not found" % UUT_IP) 
    except socket.error as msg:
        print("Socket Error: %s" % msg)
        print("No this UUT: %s" % UUT_IP) 
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

    except TypeError as msg:
        print("Type Error: %s" % msg)   
    finally: 
        s.close() 

def get_response(UUT_IP, UUT_cmd): #get control and has response
    global UUT_IPScans
    UUT_IPScans=[]
    try:
        port = 80808      
        s = socket.socket()             # Create a socket object
        host = socket.gethostname()     # Get local machine name
        UUT_Return=""
        s.settimeout(2)
        s.connect((UUT_IP, port))    #s.connect((host, port)) 
        s.settimeout(5)
        remote_cmd_str = UUT_cmd # str(input("\nplease input the cmd (default is help): \n") or "help")
        remote_cmd = remote_cmd_str.encode('utf-8')
        if not remote_cmd.lower():    #for receive others data
            print("Do nothing")
        else:
            s.send(remote_cmd)   #S1

        recv_data = s.recv(1024)    #R1, buffer not enough
        if not recv_data:
            print("no data")
            #break
        else: #get (host, IP, MAC) from UUT
            getStr=recv_data.decode("utf-8")
            UUTinfo=getStr.split(",")
            UUT_IPScans.append(UUTinfo[2])
            print ("\nReceive... \n"+ getStr)
            recv_data = s.recv(1024)  # keep waiting for data coming. Bug at here
            if not recv_data:
                s.close()
                #break
            time.sleep(1)
        s.close()
    except socket.timeout as msg:
        pass
        #print("%s is not found" % UUT_IP) 
    except socket.error as msg:
        print("Socket Error: %s" % msg)
        print("No this UUT: %s" % UUT_IP) 
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except TypeError as msg:
        print("Type Error: %s" % msg)   
    finally: 
        s.close() 

def main_menu():
    global UUT_IPs
    global UUT_IPScans

    list=["test", "test2", "test3"]
    print("""
     -----------------------------------------------------------------
     |                    Server/Client Test               |
     -----------------------------------------------------------------
         %s                    %s

     -----------------------------------------------------------------
     |  Q. Exit   {0}                                |
     |  {1}                             |
     -----------------------------------------------------------------

        """.format((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "Host/Controller IP:"+socket.gethostbyname(socket.getfqdn())) 
        %("A. Scan UUT", "*2. Kill all of task"))

    UUT_cmd = str(input("\nplease input the cmd (default is 14): \n") or "14") 
    if not UUT_cmd.lower():
        print("Do nothing")
    elif (UUT_cmd.lower() == "a"):
        UUT_cmd="__scan_uut__"
        UUT_IPs=[] #Clean all IP in UUT_IPs 
        try:
            ipRange = str(input("\nplease input the IP range (ex: 192.168.0.*), I will scan IP 192.168.0.1-254 (default is \"192.168.0.*\"): \n") or "192.168.0.*")
            ipRangeBody = ipRange.replace("*","")
            for i in range(1,255,1):
                UUT_IPs.append(str(ipRangeBody+str(i)))
            #print(UUT_IPs)
            #print("Total IP:",UUT_IPs.__len__())
        except:
            print("Error, only support C class")
            UUT_IPs=""
    elif (UUT_cmd.lower() == "2"):
        UUT_cmd="taskkill /F /IM bit.exe /IM Heaven.exe /IM browser_x86.exe /IM FurMark.exe /IM java* /IM 3DMark* /IM ThermalAnalysisToolCmd* /IM Prime95* /IM STPM* /IM ffxv.exe /IM wmplayer.exe /IM nvp* /T"
    elif (UUT_cmd.lower() == "11"):
        DateNow=datetime.datetime.now().strftime("%m-%d-%y")
        TimeNow=datetime.datetime.now().strftime("%H:%M:%S")
        #date mm-dd-yy |time hh:mm:ss
        UUT_cmd="date "+DateNow+"|time "+TimeNow
        print("Now "+DateNow+" "+TimeNow)
    elif (UUT_cmd.lower() == "13"):
        UUT_cmd=""
        try:
            filename = str(input("\nplease input the file (default is IP.txt): \n") or "IP.txt")
            with open(filename, "r") as f:
                IP_table=f.read().splitlines()
            f.close()
            UUT_IPs=IP_table
            print(UUT_IPs)
        except:
            print("File not found")
            UUT_IPs=""
    elif (UUT_cmd.lower() == "14"):
        UUT_cmd=""
        print("IP lists:")
        for IP in UUT_IPs:
            print(IP)
        print("Total IP:",UUT_IPs.__len__())
    elif (UUT_cmd.lower() == "15"):
        UUT_cmd="shutdown -r -f -t 0"
    elif (UUT_cmd.lower() == "22"):
        UUT_cmd=""
        IP_export=""
        for IP in UUT_IPs:
            IP_export=IP_export+IP+"\n"
            print(IP)
        ip = open("IP_export.txt","w",encoding="utf-8")
        ip.write(IP_export)
            #IP_export.write(ip)
        ip.close()
        print("Export IP to IP_export.txt")
    elif (UUT_cmd.lower() == "help"):
        UUT_cmd=""
        help()
    elif (UUT_cmd.lower() == "exit" or UUT_cmd.lower() == "q" or UUT_cmd.lower() == "qq"):
        print("Goodbye")
        sys.exit(0)
    
    #single thread method 1, use this
    if len(sys.argv)>1:
        #single UUT
        UUT_IP=sys.argv[1]
        try:
            UUT_Return = str(get_control(UUT_IP,UUT_cmd)) #ip, cmd
            if UUT_Return=="U:OK, just do it.":
                print("C:OK")
            else:
                print("C:UUT_Return:",UUT_Return)
        except:
            print(UUT_IP,"connection fail.")
    else: #multi thread
        if UUT_IPs=="": #
            print("No IP input")
        elif UUT_cmd=="":
            pass
            #print("No command")
        elif UUT_cmd=="__scan_uut__": #for scan uut
            threads=[]
            for UUT_IP in UUT_IPs:
                try:
                    threads.append(threading.Thread(target=get_response,args=(UUT_IP,UUT_cmd)))
                    try:
                        threads[UUT_IPs.index(UUT_IP)].start()
                    except timeout:
                        print("thread connection fail.")
                except:
                    print(UUT_IP,"connection fail.")
            for UUT_IP in UUT_IPs:
                threads[UUT_IPs.index(UUT_IP)].join()
            UUT_IPs=UUT_IPScans # replace IP list by scan IP
        else:
            #for multi UUT
            threads=[]
            #command to all of UUT
            for UUT_IP in UUT_IPs: 
                #while True:
                #print(UUT_IP)
                try:
                    #UUT_Return = str(threads.append(threading.Thread(target=get_control,args=(UUT_IP,UUT_cmd))))
                    threads.append(threading.Thread(target=get_control,args=(UUT_IP,UUT_cmd)))
                    try:
                        threads[UUT_IPs.index(UUT_IP)].start() 
                        
                        #if UUT_Return=="U:OK, just do it.":
                        #    print("C:OK")
                        #else:
                        #    print("C:UUT_Return:",UUT_Return)                        
                    except timeout:
                        print("thread connection fail.")                   
                except:
                    print(UUT_IP,"connection fail.")
            for UUT_IP in UUT_IPs:
                threads[UUT_IPs.index(UUT_IP)].join()

def help():
    print("""
This is help...
        """)

def scan_uut():
    pass
if __name__ == "__main__":  # Start from here
    os.system('mode con: cols=80 lines=30')
    UUT_IPs=["192.168.1.178","192.168.1.22","192.168.1.31","192.168.0.34"]
    while True:
        main_menu()
