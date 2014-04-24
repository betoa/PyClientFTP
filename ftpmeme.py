import socket
import time
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#main socket
#***************************************
def sendcmd(cmd):
  global s
  s.send(cmd+"\r\n")
#***************************************
def getline():
  global s
  return s.recv(1024)
#***************************************
def execute(cmd):
  sendcmd(cmd)
  return getline()
#***************************************
#command executing sequence and delay is important in this module
def getpasv(cmd):
  global s
  ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  #temporary socket for pasv connection.
  a=execute("PASV")
  print (a)
  print ("connecting to %s:%d" % parse(a))
  ss.connect(parse(a))
  sendcmd(cmd)
  fhandle=open("d:\\a.rar","wb")#replace d: with e: for memory card if pys60
  while 1:
    tmp = ss.recv(1024)
    if not tmp:
      break;
    fhandle.write(tmp)
  fhandle.close()
  ss.close()
  time.sleep(1) #this delay is required
  return getline()
#***************************************
def parse(st):
  x=st[st.rindex("(")+1:st.rindex(")")]
  y=x.split(",")
  ipaddr=y[0]+"."+y[1]+"."+y[2]+"."+y[3]
  portnum=(int(y[4])*256)+int(y[5])
  return ipaddr,portnum
#***************************************
print ("program started")
try:
  s.connect(('192.100.230.21',21))
  print (getline())
  print (execute("USER userftp"))
  print (execute("PASS r3d3sf1s1c@s"))
  print (execute("CLNT FileZilla"))
  print (execute("OPTS UTF8 ON"))
  print (execute("CWD /Tools"))
  print (execute("PWD"))
  print (execute("TYPE I"))
  print (getpasv("RETR datarecovery.rar"))
  print (execute("QUIT"))
  s.close()
except socket.error as e:
  print ("ERROR: %s" % e)
print ("done!")
#***************************************
