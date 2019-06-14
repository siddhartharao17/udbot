#!/usr/local/bin/python3
import socket
import requests

# This block creates a socket and connects to the IRC server
ircsockObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = 'chat.freenode.net'
port = 6667
channel = '#testchan'
botname = 'sid'

print("Connecting to Freenode...")
try:
    ircsockObj.connect((server, port))
except socket.error as e:
    ircsockObj.close()
    print("[-] Unsuccessful connection to IRC server!")
    raise
ircsockObj.send(bytes("USER " + botname + " * * :UrbanDictBot\n", "UTF-8"))  # USER udbot 8 * :Ronnie Reagan
ircsockObj.send(bytes("NICK " + botname + "\n", "UTF-8"))
print("[+] Bot connected to Freenode.")
# -------------------------------------

def joinChannel(channel):
    # Once the bot joins the channel, it will receive information
    # about notices and commands it can use, so we need to capture that.
    print("[+] Joining channel #testchan...")
    ircsockObj.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsockObj.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
    print("[+] Bot joined channel #testchan.\n\n")

def ping(pingServer):
    # respond to server Pings.
    ircsockObj.send(bytes("PONG " + pingServer + "\n", "UTF-8"))
    print("PONG sent back to " + pingServer)

def sendMsgToChannel(msg):
    # print(msg)
    ircsockObj.send(bytes("PRIVMSG " + channel + " :" + msg + "\n", "UTF-8"))     # PRIVMSG #testchan :msg

def ud(udquery):
    APIURL = 'http://api.urbandictionary.com/v0/define'
    PARAMS = {'term': udquery}
    r = requests.get(url=APIURL, params=PARAMS)
    response = r.json()
    # print(response)
    definition = response['list'][0]['definition']
    sendMsgToChannel(definition)

def body():

    while 1:
        ircmsg = ircsockObj.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        if ircmsg.find(".ud") != -1:
            # query = ircmsg
            ircmsg = ircmsg.split('.ud ')
            if len(ircmsg) != 2:
                sendMsgToChannel("[-] Incorrect syntax. Usage: .ud <search_term>")
                continue

            query = ircmsg[1]
            # print(query)
            ud(query)

        # Check if the information we received was a PING request. If so, we call the ping() function we defined earlier so we respond with a PONG.
        elif ircmsg.find("PING :") != -1:
            ircmsg = ircmsg.split(' :')
            pingServer = ircmsg[1]
            print("PING received from " + pingServer)
            # pingServer =
            ping(pingServer)

def main():
    joinChannel(channel)    # This will join the bot to the channel
    body()


if __name__ == '__main__':
    main()
