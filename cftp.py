#
#Cliente FTP en Python
#by: Humbero Arreola
#

import socket               
import sys
import os
import time
import string
import array
import ssl, pprint, getpass, telnetlib

nws = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
usr = socket.socket(socket.SOCK_STREAM, socket.SOCK_STREAM)

def connect21():
    try:
        host = input('HOST: ')
        print('***Connecting to '+host+':21***')
        time.sleep(.5)
        s.connect((host, 21))
        print (s.recv(1024))
        user()
        passwd()
        #**********USER + PASSWD , intento
##        print ('USER: ')
##        user = sys.stdin.readline()
##        print ('PASSWD: ')
##        password = sys.stdin.readline()
###       send("USER "+user[:-1])
##        usr.connect((user,password))
##        time.sleep(2) #pausa para no recibir muy rapido
## #       send(user)
##        rec = s.recv(1024)
##        if "230 " in rec:
##                print("Password accepted!")
##                print (recv(1024))
##        else:
##                print ("Password not accepted")
        #***********
#       s.close                     #Cerrar Socket
    except socket.error as error:
        print('*******Server Error*******\n') %(error)
        pass

def connect():
    try:
        host = input('HOST: ')
        ##Ports MENU
        print ("-"*60)
        print ("Specify port to host: "+host)
        #**** OPTION 1
##        print ("""
##        1)Use default list
##        2)Specify your own port list""")
##        print ("-"*60)
##        opt2 = int(input("Please choose an option\n"))
##        if opt2 == 1:
##            #puerto por default
##            ports = (22, 23, 24, 25, 80, 110, 135, 139, 443, 445, 553, 3306, 3389, 8080)
##        if opt2 == 2:
##            ports = input("Please enter the ports you would like scanned.\neg. 22, 23\n>>")
##        print ("Ok, here we go..")
##        
##        ports = [int(port.strip()) for port in ports.split(',')]
##
##        for port in ports:
##            #abrir socket con el nuevo puerto
##            connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
##            connect.connect_ex((host, port))
        #*****
        port = int(input('PORT: '))
        print ("-"*60)
        time.sleep(.4)
        nws.connect_ex((host,port))#socket declarado al principio del codigo        
        print (nws.recv(1024))
        user()
        passwd()
    except socket.error as error:
        print('*******Server Error*******\n') %(error)
        pass

def send(us):
	s.sendall(us + "\n") 

##++LOGIN2 (USER, PASSWD) ++++++++
def user():
        print ('USER: ')
        user = sys.stdin.readline()
#       send("USER "+user[:-1])
        s.sendall((user))
        time.sleep(2) #pausa para no recibir muy rapido
#       send(user)
        rec = (s.recv(1024))
        if "331 " in rec:
                passwd() #Usuario valido, pedir password
        else:
                print ("Invalid username") #usuario invalido
#ERROR AL TRANSMITIR USER: 'str' does not support buffer interface!!
                
def passwd():
	print ('PASSWORD: ')
	password = sys.stdin.readline()
	s.sendall(password)
	tim.sleep(1)
	rec = s.recv(1024)
	if "230 " in rec:
		"Password accepted!"
		print (recv(1024))
	else:
		print ("Password not accepted")

#*********
		
def loggit():
	timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #Make timestamp
	log.write(timestamp + " " + s + '\n')
	
#LISTADO
def list():
	print ("What file would you like to use?")
	sendstr = sys.stdin.readline()
	s.sendall(sendstr)
	print ("Please wait..")
	time.sleep(10)
	rec = s.recv(1024)
	if "450 " in rec:
		print ("No File..")
	elif "150 " in rec:
		print ("Sending ascii list")
		output = open("list", "wb")
		loggit("File, list opened")
		loggit("Reading file data from socket...")
		#Start write loop
		while 1:
			filedata = nws.recv(1024) #receive data from socket
			if not filedata:
				#if there is no data being read, exit the loop
				break;
			else:
				loggit("File data: " + filedata)
				output.write(filedata) #write the output to a file
		print ("File transferred!")
		output.close() #close the file
		loggit("File, list closed")
	else:
		print (s.recv(1024))
#*****
def recv_archivo(s,archivo):
    timeout=1
    s.setblocking(0)
    Rdatos=False #datos recibidos
    inicio=time.time()
    archivo = open(archivo, 'archivo')
    while True:
        if Rdatos and time.time()-inicio>timeout:
            break
        try:
            datos=s.recv(1024)
            if datos:
                Rdatos = True
                archivo.write(datos)
              
                inicio=time.time()
            else:
                time.sleep(1)
        except:
            pass
    archivo.close()

#****
#*****MAIN****

if __name__ == '__main__':

    try:
        opt = int(1)
        while opt != 0:
                print ("-"*60)
                print ("                    CLIENT FTP")
                print ("-"*60)
                print ("""                1. Connect via FTP (Port 21)
                2. Connect via FTP (Different Port)
                3. Know IP of and Address """)
                print("-"*60)
                opt = int(input("Choose an Option-> "))
                if opt == 1:
                    connect21()
                if opt == 2:
                    connect()
                if opt == 3:
                    ip = socket.gethostbyname(input('Address: '))
                    print('IP: '+ip+'\n')
    except socket.error as err:
        print('**Socket ERROR** \n')%(err)
        pass
