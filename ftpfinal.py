import socket
import time
import getpass

menu = '''
-------------------------------------
            CLIENT FTP
-------------------------------------
MENU
1. Connect to Server via FTP (port 21) 
2. Connect to Server via FTP (different port)
3. Know IP of and Adress (DNS)
-------------------------------------
Option -> '''

lista = '''
--------------------------------------
            COMMANDS LIST        
--------------------------------------
logout              # Exit 
cd (directory)      # Change Directory
ls                  # List Directory
upload (filename)   # Upload a File 
download (filename) # Download a File 
mkdir (directory)   # Make Directory
pwd                 # Working Directory
rmd                 # Remove Directory
rm (filename)       # Remove File
--------------------------------------
Option -> '''

               
def recv_timeout(s,timeout=2):
    s.setblocking(0)
    total_data=[];data='';begin=time.time()
    while True:
        if total_data and time.time()-begin>timeout:
            break
        elif time.time()-begin>timeout*2:
            break
        try:
            data=s.recv(1024)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return data.join(total_data)

def recv_file(s,filename,timeout=1):
    s.setblocking(0)
    somedatarecved=False;data='';begin=time.time()
    f = open(filename, 'wb')
    while True:
        if somedatarecved and time.time()-begin>timeout:
            break
        elif time.time()-begin>timeout*2:
            break
        try:
            data=s.recv(1024)
            if data:
                somedatarecved = True
                f.write(data)
                f.flush()
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    f.close()

def request(s, message):
    request = message + '\r\n'
    print (request)
    request1 = request.encode('UTF-8')
    s.sendall(bytes(request1))
    
    response = recv_timeout(s)
    print (response)
    return response

def open_socket(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(s.recv(1024))
    return s

def pasv_socket(s):
    response = request(s, 'PASV')
    if not process_response(response, 'PASV'):
        return None
    
    iptext = response.split(' ')[4].replace('(', '').replace(')','').split(',')
    HOST = '%(1)s.%(2)s.%(3)s.%(4)s' % { '1' : iptext[0], '2' : iptext[1], '3' : iptext[2], '4' : iptext[3] }
    PORT = int(iptext[4]) * 256 + int(iptext[5])
##    m = response.search(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', reply[1])
##    s.dataAddr = (m.group(1) + '.' + m.group(2) + '.' + m.group(3) + '.' + m.group(4), int(m.group(5)) * 256 + int(m.group(6)))
##    s.dataMode = 'PASV'
##    HOST = '%(1)s.%(2)s.%(3)s.%(4)s' % { '1' : m.group(1), '2' : m.group(2), '3' : m.group(3), '4' : m.group(4) }
##    PORT = int(m.group(4) * 256 + int(m.group(5)))
               
    return open_socket(HOST, PORT)

def process_response(response, command):
    comandos = { 'USER' : [331], 'PASS' : [230], 'CONN' : [220], 'PWD'  : [257], 'CWD'  : [250], 'RMD'  : [250], 'MKD'  : [257], 'LIST' : [150,226], 'RETR' : [150,226], 'STOR' : [150,226], 'PASV' : [227], 'QUIT' : [221], 'DELE' : [250] }
    if response == '':
        return False
    valido = True
    for a in response.splitlines():
        if int(response[0:3]) not in comandos[command]:
            valido = False
            break
    return valido
    
def ls(s):
    file_socket = pasv_socket(s)
    if file_socket == None:
        print ('Operation failed')
        return False

    if not process_response(request(s, 'LIST'), 'LIST'):
        print ('Operation failed')
        return False
    
    print (recv_timeout(file_socket))

    file_socket.close()

def login(s):
    user = str(input('User: '))
    passw = str(input('Password: '))
    print('Logging In...')
#    user = 'userftp'
#    passw = 'r3d3sf1s1c@s'
    if not process_response(request(s, 'USER ' + user), 'USER'):
        print ('Invalid user')
        return False
    if not process_response(request(s, 'PASS ' + passw), 'PASS'):
        print ('Invalid password')
        return False
    print ('Successfully logged in')
    return True

def logout(s):
    ret = True
    if not process_response(request(s, 'QUIT'), 'QUIT'):
        print ('Quit operation falied')
        ret = False
    s.close()
    print ('Successfully logged out')
    return ret

def cd(s, path):
    if not process_response(request(s, 'CWD ' + path), 'CWD'):
        print ("Can't change directory to " + path)
        return False
    print ('Ok')
    return True
        
def pwd(s):
    response = request(s, 'PWD')
    if not process_response(response, 'PWD'):
        print ('Operation failed')
        return False
    print (response[4:])
    return True
    
def mkd(s, dir):
    if not process_response(request(s, 'MKD ' + dir), 'MKD'):
        print ("Can't create a directory with such a name")
        return False
    print ('Ok')
    return True
    
def rmd(s, dir):
    if not process_response(request(s, 'RMD ' + dir), 'RMD'):
        print ("Can't remove a directory with such a name")
        return False
    print ('Ok')
    return True        
    
def upload(s, filename):
    file_stream = pasv_socket(s)
    if file_stream == None:
        print ('Operation failed')
        return False
    
    if not process_response(request(s, 'STOR ' + filename), 'STOR'):
        print ("Can't upload file to ftp")
        return False
    
    buffer = "hello"
    f = open(filename, 'rb')
    while True:
        buffer = f.read(1024)
        if buffer == "":
            break
        file_stream.send(buffer)
    f.close()
    file_stream.close()
    print (recv_timeout(s))
    print ('Ok')
    return True

def download(s, filename):
    file_stream = pasv_socket(s)
    if file_stream == None:
        print ('Operation failed')
        return False
        
    if not process_response(request(s, 'RETR ' + filename), 'RETR'):
        print ("Can't download file from ftp")
        return False
    
    recv_file(file_stream, filename+"_")
    file_stream.close()
    print (recv_timeout(s))
    print ('Ok')
    return True
    
def rm(s, filename):
    if not process_response(request(s, 'DELE ' + filename), 'DELE'):
        print ("Can't remove a file with such a name")
        return False
    print ('Ok')
    return True
    
def connect():
    HOST = input('HOST: ')
    PORT = int(input('PORT: '))
    print('Connecting...')
#    HOST = '192.100.230.21'
#    PORT = 21
    socketc = open_socket(HOST, PORT)
    login(socketc)

    return socketc
def connect21():
    HOST = input('HOST: ')
#        HOST = '192.100.230.21'
    print('Conecting to '+HOST+':21')
    socketc = open_socket(HOST,21)
    login(socketc)
    return socketc

if __name__ == '__main__':
    
    socketc = None
    print(menu)
    opt = int(input())
    if opt == 1:
        socketc = connect21()
    if opt == 2:
        socketc = connect()
    if opt == 3:
        ip = socket.gethostbyname(input('ADDRESS: '))
        print('IP: '+ip)
        socketc = connect()
    else:
        socketc = connect()

    while True:
        print(lista)
        opc = str(input()).split(' ')
        command = opc[0]
        
        if command == 'pwd':
            pwd(socketc)
        elif command == 'cd':
            cd(socketc, opc[1])
        elif command == 'ls':
            ls(socketc)
        elif command == 'mkdir':
            mkd(socketc, opc[1])
        elif command == 'rm':
            rm(socketc, opc[1])
        elif command == 'rmd': 
            rmd(socketc, opc[1])
        elif command == 'upload':
            upload(socketc, opc[1])
        elif command == 'download':
            download(socketc, opc[1])
        elif command == 'logout':
            logout(socketc)
            exit()
        else:
            print ('Invalid Option')
