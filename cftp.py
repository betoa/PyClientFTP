#
#Cliente FTP en Python
#by: Humbero Arreola
#

import socket               
import sys
import time
import string
import time
import array
import base64

nws = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        s.connect((input('HOST: '),int(input('PORT: '))))
        print (s.recv(1024))
#       s.close                     #Cerrar Socket
    except socket.error as error:
        print('*******Server Error*******\n') %(error)
        pass

#****************
#*** LOGIN 1   +++++++++
##def login():
##        user = (input('USER: '))
##        passwd = (input('PASSWORD: '))
##        userb = user.encode('utf-8')
##        passwdb = passwd.encode('utf-8')
##        print(userb, passwdb)
##        token = (base64.encodestring('%s:%s' % (userb, passwdb)).strip())
##        s= socket.socket()
##        s.connect(('192.100.230.21', 80))
##        f= s.makefile('rwb', bufsize=0)
##        f.write('\r\n'.join(lines)+'\r\n\r\n')
##        response= f.read()
####        f.close()
####        s.close()


##++LOGIN2 (USER, PASSWD) ++++++++
def user():
	print ('USER: ')
	user = sys.stdin.readline()
	s.sendall(user)
	time.sleep(1) #pausa para no recibir muy rapido
	rec = s.recv(1024)
	if "331 " in rec:
		passwd() #Usuario valido, pedir password
	else:
		print ("Invalid username") #usuario invalido

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

#****
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
    
if __name__ == '__main__':

    print('1. Conectar a FTP')
    opt = int(input())
    if opt == 1:
        connect()
##        login()
        user()
        passwd()
            
    
