import socket
import string
import varsl
import re
global channel
global irc
global line
global user
global owner
global kill
irc = varsl.irc
cmdlist=("ping","say","disconnect","switch","hello","reload","cutwire","kick","debug","kill","cmd","sendall","list")
kill = False
owner = varsl.owner
def send_msg(chan,msg):
        irc.send("PRIVMSG "+chan+" :"+msg+"\r\n")
def cmd_ping(): 
        irc.send("PRIVMSG "+channel+" :PONG\r\n")
        
def cmd_say():          
        say=""  
        if(len(line)<5):
                irc.send("PRIVMSG "+channel+" :Usage: say <msg>\r\n")
                return False
        for x in range(4,len(line)):
                say+=line[x]+" "
        irc.send("PRIVMSG "+channel+" :"+say+"\r\n")
        
def cmd_disconnect():
        if(user==owner):
                return True
        else:
                irc.send("PRIVMSG "+channel+" :"+user+", you are not my master.\r\n")
def cmd_switch():
        global channel
        if(len(line)<6):
                irc.send("PRIVMSG "+channel+" :Usage: -#switch <channel> <operator>\r\n")
                return False
        if(user==owner):
                irc.send ( "PART "+channel+"\r\n" )
                irc.send ( 'JOIN %s\r\n' %line[4])
                varsl.operator=string.lower(line[5]) in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

                varsl.channel=line[4]
                channel = line[4]
        else:
                irc.send("PRIVMSG "+channel+" :"+user+", you, are not my master.\r\n")
def cmd_hello():
        irc.send("PRIVMSG "+user+" :Hello there, "+user+"\r\n")
def cmd_reload():
        if(user==owner):
                irc.send("PRIVMSG "+channel+" :"+user+": Reloaded!.\r\n")
def cmd_cutwire():
        if(len(line)<5):
                irc.send("PRIVMSG "+channel+" :Usage: -#cutwire <letter>\r\n")
                return False
        irc.send("PRIVMSG "+channel+" :$"+line[4]+"\r\n")
def cmd_kick():
        if(user!=owner):
                send_msg(channel,"You must be my master to send this command, "+user)
                return False
        if(len(line)<6):
                irc.send("PRIVMSG "+channel+" :Usage: -#kick <user> <msg>\r\n")
                return False
        say=""
        for x in range(5,len(line)):
                say += line[x]+ " "
        irc.send ( "KICK "+channel+" "+line[4]+" :"+say+"\r\n" )
        
def cmd_debug():
        if(user==owner):
                varsl.debug=not varsl.debug
                return False
        else:
                send_msg(channel,"You must be my master to send this command, "+user)
def cmd_kill():
        global kill
        if(user!=owner):
                send_msg(channel,"You must be my master to send this command, "+user)
                return False
        if(kill):
                send_msg(channel,"Im done killing")
        else:
                send_msg(channel,"KILL TIME")
        
        kill = not kill
def cmd_cmd():
        if(user!=owner):
                send_msg(channel,"You must be my master to send this command, "+user)
                return False
        if(len(line)<6):
                irc.send("PRIVMSG "+channel+" :Usage: -#cmd <cmd> <arguments>\r\n")
                return False
        say=""
        for x in range(5,len(line)):
                say += line[x]+ " "
        irc.send ( string.upper(line[4]) +" "+ say+"\r\n" )
        send_msg(owner, "SENT: "+ string.upper(line[4]) +" "+ say )
def cmd_sendall():
        if(user!=owner):
                send_msg(channel,"You must be my master to send this command, "+user)
                return False
        if(varsl.sendAll):
                send_msg(channel,"I'm done sending the channel's conversation to your inbox.")
        else:
                send_msg(channel,"I will now send the channel's conversation to your inbox.")
        
        varsl.sendAll = not varsl.sendAll
def cmd_list():
        flist=""
        for command in cmdlist:         
               flist+="-#"+command+", "
        send_msg(channel,flist)
def say_tribot200():
        send_msg(user,"Herpdurp")

def cmd_nick():
        send_msg(channel,"My nick is Tribot200!")
        
        

def processcommand(cmd):
        global channel
        global line
        global user
        global irc      
        channel = varsl.channel 
        line = varsl.line
        user = varsl.user
        irc = varsl.irc
        a= not eval(cmd)()
        return a
def processmessage(msg):
        global channel
        global line
        global user
        global irc      
        channel = varsl.channel 
        line = varsl.line
        user = varsl.user
        irc = varsl.irc
        if (line[3] == "ACTION"):
                pos =4
        else:
                pos = 3
                p0 = re.compile('.*l.+l[a-z]+', re.IGNORECASE)
                p1 = re.compile('.*p.+p[s,z]*', re.IGNORECASE)
                p2 = re.compile('.*pa+w+[a-z]*', re.IGNORECASE)
        for i in range(pos,len(line)):
                if((p0.match(line[i]) or p1.match(line[i]) or p2.match(line[i]) or "yoshi" in string.lower(line[i]) or "yoshi" in string.lower(user)) and (user != varsl.owner and user !="StewieGriffin") and kill):
                        print "die"
                        say = line[i].lstrip(":")
                  
                        if (not varsl.operator):
                                irc.send ( "PRIVMSG "+channel+" :$timebomb "+user+"\r\n" )
                                send_msg(channel,"YOU SAID: "+say)
                        else:
                                irc.send ( "KICK "+channel+" "+user+" :"+say+"\r\n")
                        say = ""
        try:
                eval("say_"+msg)()
        except:
                FILLERVAR=0
                
                
        
