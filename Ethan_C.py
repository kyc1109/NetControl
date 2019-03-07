#!/usr/bin/python3
#coding=utf8
#sys.setdefaultencoding('utf8')

#主控端, 需求:能遠端執行命令或資料夾

import socket, os, sys, time, datetime, threading         # Import socket module
from subprocess import Popen   #http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
from importlib import reload
reload(sys)
#sys.setdefaultencoding('utf8')
# -*- coding: UTF-8 -*-
def get_control(UUT_IP, UUT_cmd):
    try:
        #0==================================
        port = 60001      
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
        #10.110.146.77
        #10.110.136.52
        #10.110.136.159
        #10.110.145.250
        #10.110.146.9
        #192.168.0.178
        #10.110.141.78

        #s.send(b"Hello UUT!") #S0  UUT 掛掉的地方


        #2==================================



        #while True :
        #remote_cmd_str = input("\nplease input the cmd (default is dir): \n") #"please input the cmd (default is dir):", "dir"
        remote_cmd_str = UUT_cmd # str(input("\nplease input the cmd (default is help): \n") or "help")
        remote_cmd = remote_cmd_str.encode('utf-8')
        if not remote_cmd.lower():    #for receive others data
            print("Do nothing")
            """
            print("hang here")
            recv_data = s.recv(1024) #hang on here
            if not recv_data:
                print("No data")
            else:
                recv_data = s.recv(1024)
                print ("\nReceive... \n"+ recv_data)      
            """
        elif remote_cmd.lower() == "exit" or remote_cmd.lower() == "q":
            s.send(b"Close by client")
            s.close()
        else:
            s.send(remote_cmd)   #S1
            #print('H:Sending... ',repr(remote_cmd_str)) #2/26 remove cmd to U

        time.sleep(1)   #delay
        """
        recv_data = s.recv(1024)    #R1, buffer not enough
        if not recv_data:
            print("no data")
            break
        else:
            print ("\nReceive... \n"+ recv_data)
            recv_data = s.recv(1024)  # keep waiting for data coming. Bug at here
            if not recv_data:
                s.close()
                break
            time.sleep(1)
        """
        try:#response from UUT
            s.setblocking(0)
            total_data="";data="";begin=time.time();timeout=2
            UUT_Return = s.recv(1024).decode("utf-8")
            #print("remote:",UUT_Return) #2/26 remove ack from U
        except:
            print("Command error")
         #str type with decode.
        """
        while True: #1
            if total_data and time.time()-begin>timeout:
                break
            elif time.time()-begin>timeout*2:
                break
            try:
                data=s.recv(1024) #1024, Type Error: must be str, not bytes
                #print("data recv")
                if data is not None:
                    total_data=total_data+data.decode("utf-8","ignore")
                    #print("data ++")
                    begin=time.time()
                else: 
                    time.sleep(0.1)
            except Exception as e:
                raise e
            #print("total_data")
            print("remote:",total_data) #show txt feedback of UUT, total_data.decode('gb2312', 'ignore').encode('utf-8')
            
            #wf = open("total_data.txt",'w')  #write file TestItem4_1.txt ~ TestItem4_11.txt
            #for w in total_data:   #var TestItem4_1~TestItem4_11
            #    wf.write(w.decode('gb2312', 'ignore').encode('utf-8'))                       #write TestItem4_1 to TestItem4_1.txt, TestItem4_2 to TestItem4_2.txt ...
            #wf.close()
        """
        return UUT_Return 
        s.close()
            #break
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
        #print("Sever: " +s.recv(1024))
        s.close() 
        
        #print('finally connection closed')
        #print("press any key for input next command")
        #os.system("pause")
#p=Popen('received_file.bat')
#stdout,stderr =p.communicate()


def main_menu():
    global UUT_IPs
    #10.110.146.77
    #10.110.136.52

    list=["test", "test2", "test3"]
    print("""
     -----------------------------------------------------------------
     |               Stress Test Menu      DQA IoT/A73               |
     -----------------------------------------------------------------
         %s                     %s
         %s                           %s
         %s                           %s
         %s                           %s
         %s                %s
        %s           %s
        %s            %s
        %s
     -----------------------------------------------------------------
     |  Q. Exit   {0}                                |
     |  {1}                             |
     -----------------------------------------------------------------

        """.format((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "Host/Controller IP:"+socket.gethostbyname(socket.getfqdn())) 
        %("A. Scan UUT", "2. Send cmd", 
            "3. S3", "4. S4",
            "5. S5","6. MS", 
            "7. WB", "8. HyS5",
            "9. Get UUT Info","10. Send run file",
            "11. Sync Up Date/Time", "12. Update_Stress",
            "13. Load IP txt file", "14. Show IP list",
            "15. UUT reboot"))
    UUT_cmd = str(input("\nplease input the cmd (default is 14): \n") or "14") 

    if not UUT_cmd.lower():
        print("Do nothing")
    elif (UUT_cmd.lower() == "11"):
        DateNow=datetime.datetime.now().strftime("%m-%d-%y")
        TimeNow=datetime.datetime.now().strftime("%H:%M:%S")
        #date mm-dd-yy |time hh:mm:ss
        UUT_cmd="date "+DateNow+"|time "+TimeNow
        print("Now "+DateNow+" "+TimeNow)
    elif (UUT_cmd.lower() == "12"):
        UUT_cmd="start update_stress.exe"

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
        for IP in UUT_IPs:
            print(IP)
    elif (UUT_cmd.lower() == "15"):
        UUT_cmd="shutdown -r -f -t 0"

    elif (UUT_cmd.lower() == "exit" or UUT_cmd.lower() == "q" or UUT_cmd.lower() == "qq"):
        sys.exit(0)


    """
    #Excute cmd by multi threading method 2, No good
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
    else:
        if UUT_IPs=="": #
            print("No IP input")
        elif UUT_cmd=="":
            print("No command")
        else:
            #for multi UUT
            from multiprocessing.pool import ThreadPool
            pool = ThreadPool(processes=4)
            for UUT_IP in UUT_IPs:
                #while True:
                #print(UUT_IP)
                try:
                    async_result = pool.apply_async(get_control, (UUT_IP,UUT_cmd)) # tuple of args for foo
                    UUT_Return = async_result.get()
                    if UUT_Return=="U:OK, just do it.":
                        print("C:OK")
                    else:
                        print("C:UUT_Return:",UUT_Return)
                except:
                    print(UUT_IP,"connection fail.")

    """

    
    #Excute cmd by multi threading method 1, use this
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
    else:
        if UUT_IPs=="": #
            print("No IP input")
        elif UUT_cmd=="":
            pass
            #print("No command")
        else:
            #for multi UUT
            threads=[]
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

    """
    #Excute cmd by single thread
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

    else:
        if UUT_IPs=="": #
            print("No IP input")
        elif UUT_cmd=="":
            print("No command")
        else:
            #for multi UUT
            for UUT_IP in UUT_IPs:
                #while True:
                #print(UUT_IP)
                try:
                    UUT_Return = str(get_control(UUT_IP,UUT_cmd)) #ip, cmd
                    if UUT_Return=="U:OK, just do it.":
                        print("C:OK")
                    else:
                        print("C:UUT_Return:",UUT_Return)
                except:
                    print(UUT_IP,"connection fail.")
    """





if __name__ == "__main__":  # Start from here
    os.system('mode con: cols=80 lines=80')
    UUT_IPs=["192.168.0.178","192.168.0.22"]
    while True:
        main_menu()

"""
Know issue buffer not ready ?p?G?ǤӦhdata?|lose data
"""
