import socket
import string
import commands
import varsl
import time



varsl.channel = raw_input("Give me a channel: ")
s= raw_input("Am I an OP in this channel? [true/false] ")
varsl.operator=string.lower(s) in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
print varsl.operator
channel = varsl.channel
network = 'irc.freenode.net'
nick="Tribot200"
file2 = open("password","r")

password=file2.read()
file2.close()
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
varsl.irc = irc
irc.settimeout(10)
irc.connect ( ( network, port ) )
irc.send ( 'NICK %s\r\n'%nick )
irc.send ( 'USER %s %s %s :%s\r\n' %(nick,nick,nick,nick) )
irc.send ( 'JOIN %s\r\n' %channel)
irc.send ( 'NICKSERV :identify %s\r\n'%password )
irc.send ( "PRIVMSG "+channel+" :Triclops200's bot is in the house!\r\n" )
varsl.irc=irc
print "connected"
usercount=0
prevuser=" "
start = -1

a=True
data=""
f = open("logs/"+channel,"a")
while(a):
        try:  
                data += irc.recv ( 4096 )
                temp = string.split(data,"\n")
                data = temp.pop()
                for line in temp:
                        line = string.rstrip(line) 
                        line = string.split(line)
                        if(varsl.debug):
                                print line
                        if(string.lower(line[0])=="ping"):
                                irc.send("PONG "+line[1]+"\r\n")
                                print "<PING>"
                                line=("hi","bye","nye") 
                                command=""
                        if (string.lower(line[1])=="kick"):
                                irc.send ( 'JOIN %s\r\n' %varsl.channel)
                          
                        if(string.lower(line[1])=="privmsg"):
                                command=""              
                                user=string.split(line[0],"!")[0].lstrip(':')
                                if(prevuser == user):
                                        usercount+=1
                                        if(start==-1):
                                                start = time.time()   
                                else:
                                        start = -1
                                        usercount=0
                                        prevuser = user
                                        
                                if(usercount>=4 and user != varsl.owner and time.time()- start <= 5 and start!=-1):
                                        if (not varsl.operator):
                                                irc.send ( "PRIVMSG "+channel+" :$timebomb "+user+"\r\n" )
                                        else:
                                                irc.send ( "KICK "+channel+" "+user+" :DO NOT SPAM! (5 messages in a row in less than 5 seconds)\r\n" )
                                        irc.send ( "PRIVMSG "+channel+" :"+user+": DO NOT SPAM! (5 messages in a row in less than 5 seconds)\r\n" )
                                        usercount=0
                                if(time.time()- start>5):
                                        usercount=0
                                        start = -1
                                message= "<"+user+">: "
                                say = ""
                                for x in range(3,len(line)):
                                        say+=line[x]+" "                
                                f.write(message+say.lstrip(":")+"\r\n")
                                if(varsl.sendAll):
                                        irc.send("PRIVMSG "+varsl.owner+" :"+message+say.lstrip(":")+"\r\n")
                                f.flush()
                                print message+say.lstrip(":")
                                if("pop" in string.lower(line[3]) and user!= varsl.owner):
                                        print "lolipopz"
                                        irc.send ( "KICK "+channel+" "+user+" :lolipoz\r\n" )
                                if(line[3].startswith(":-#")):
                                
                                        command = string.lower("cmd_"+string.split(line[3],"#")[1])
                                        if(command=="cmd_reload" and user=="triclops200"):
                                                channel=varsl.channel
                                                reload(varsl)
                                                reload(commands)
                                                varsl.channel = channel
                                                varsl.irc = irc
                                        print "<"+string.upper(command)+">: USER: "+user
                                        varsl.user = user
                                        varsl.line = line
                                        a=commands.processcommand(command)
                                else:
                                        varsl.user = user
                                        varsl.line = line
                                        commands.processmessage(line[3].lstrip(':'))
        except Exception as inst:
                        print inst

irc.send ( "PART "+varsl.channel+"\r\n" )
irc.send ( 'QUIT\r\n' )


irc.close()
