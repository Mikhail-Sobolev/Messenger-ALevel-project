import socket 
import threading
import inetabst.inetl as inetl

HOST = "127.0.0.1"
PORT = 65432

accounts = [{"username":"misha",  "password":"a","id":"0001","friends":["0004","0002","0003","0005","0006"]},
            {"username":"nef",    "password":"b","id":"0002","friends":["0001","0004","0003"]},
            {"username":"cory",   "password":"c","id":"0003","friends":["0001","0002","0004","0005","0006"]},
            {"username":"adam",   "password":"d","id":"0004","friends":["0001","0002","0003","0005","0006"]},
            {"username":"stanley","password":"e","id":"0005","friends":["0001","0003","0004","0006"]},
            {"username":"rowan",  "password":"f","id":"0006","friends":["0001","0003","0004","0005"]}]

chatrooms = [{"server":"0000","name":"general","id":"0000","users":[],"messages":[]},{"server":"0000","name":"links","id":"0001","users":[],"messages":[]},{"server":"none","name":"Groupchat","id":"0002","users":["0000","0001","0002"],"messages":[]}]
servers = [{"name":"T.D Solovjov RC","id":"0000","users":["0001","0004","0002","0003"],"chatrooms":["0000","0001"]}]

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(5)

print(" *   server start")

def handle_client(client):
    global accounts
    is_loged_in = False
    c_acc = None
    c_chatroom = None
    while True:
        c_pack = inetl.MPacket()
        s_pack = inetl.MPacket()
        s_pack.PacketIsClient = False
        c_pack.recieve(client)
        print(f" *** recv: {c_pack}")

        if c_pack.PacketType == inetl.PacketTypeClient.TC_LogIn:
            s_details = c_pack.content.split("\x00")
            print(f" *** login: {s_details}")
            if len(s_details) != 2:
                s_pack.PacketType = inetl.PacketTypeServer.TS_CheckFail
                s_pack.content = "PACK FORMAT ERROR"
                s_pack.send(client)
            elif s_details[0] not in [x["username"] for x in accounts]:
                s_pack.PacketType = inetl.PacketTypeServer.TS_CheckFail
                s_pack.content = "ACC1 NO SUCH ACCOUNT FOUND"
                s_pack.send(client)
            else:
                acc = None
                for a in accounts: 
                    if a["username"] == s_details[0]:
                        acc = a
                if acc == None:
                    s_pack.PacketType = inetl.PacketTypeServer.TS_CheckFail
                    s_pack.content = "ACC2 NO SUCH ACCOUNT FOUND"
                    s_pack.send(client)
                else:
                    if s_details[1] == acc["password"]:
                        s_pack.PacketType = inetl.PacketTypeServer.TS_CheckSuccess
                        s_pack.content = "LOGIN SUCCESS"
                        s_pack.send(client)
                        is_loged_in = True
                        c_acc = acc
                    else:
                        s_pack.PacketType = inetl.PacketTypeServer.TS_CheckFail
                        s_pack.content = "LOGIN FAILURE. INCORRECT PASSWORD"
                        s_pack.send(client)

        elif is_loged_in:
            if c_pack.PacketType == inetl.PacketTypeClient.TC_LogOut:
                s_pack.PacketType = inetl.PacketTypeServer.TS_CheckSuccess
                s_pack.send(client)
                break

            elif c_pack.PacketType == inetl.PacketTypeClient.TC_FriendList:
                packstr = inetl.SPacket()
                for f in c_acc["friends"]:
                    for acc in accounts:
                        if acc["id"] == f:
                            m_pack = inetl.MPacket()
                            m_pack.PacketType = inetl.PacketTypeServer.TS_Elem
                            m_pack.PacketIsClient = False
                            m_pack.content = f"{acc["username"]}#0x{acc["id"]}"
                            packstr.append(m_pack)
                packstr.send(client)
            elif c_pack.PacketType == inetl.PacketTypeClient.TC_ServerList:
                packstr = inetl.SPacket()
                for server in servers:
                    if acc["id"] in server["users"]:
                        m_pack = inetl.MPacket()
                        m_pack.content = f"{server["name"]}#0x{server["id"]}"
                        m_pack.PacketIsClient=False
                        m_pack.PacketType = inetl.PacketTypeServer.TS_Elem
                        packstr.append(m_pack)
                packstr.send(client)
            elif c_pack.PacketType == inetl.PacketTypeClient.TC_ChatList:
                packstr = inetl.SPacket()
                for chat in chatrooms:
                    if acc["id"] in chat["users"]:
                        m_pack = inetl.MPacket()
                        m_pack.content = f"{chat["name"]}#0x{chat["id"]}"
                        m_pack.PacketIsClient=False
                        m_pack.PacketType = inetl.PacketTypeServer.TS_Elem
                        packstr.append(m_pack)
                packstr.send(client)

        else:
            s_pack.PacketType = inetl.PacketTypeServer.TS_CheckFail
            s_pack.content = "NOT LOGGED IN USING LOGIN REQ PACKET"
            s_pack.send(client)

    client.close()

while True: 
    (CliSock,addr) = sock.accept() 
    print(f" **  accept from {addr}")

    ct = threading.Thread(target=handle_client,args=(CliSock,))
    ct.start()