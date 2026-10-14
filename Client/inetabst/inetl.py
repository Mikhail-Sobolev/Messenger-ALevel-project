
import socket
import enum

class PacketTypeClient(enum.Enum):
    TC_None = 0
    TC_LogIn = 1
    TC_LogOut = 2
    TC_ChangeDetails = 3 
    TC_ChatList = 4
    TC_ServerList = 5
    TC_MessageList = 6
    TC_ChatDetail = 7
    TC_ServerDetail = 8
    TC_MessageDetail = 9
    TC_SendMessage = 10
    TC_Elem = 11
    TC_End = 12
    TC_FriendList = 13
    TC_AddFriend = 14
    TC_UserDetail = 15
    TC_CreateChat = 16
    TC_CreateServer = 17
    TC_ChangeServerDetail = 18

class PacketTypeServer(enum.Enum):
    TS_None = 0
    TS_CheckSuccess = 1
    TS_CheckFail = 2
    TS_Elem = 3
    TS_End = 4

class MPacket:
    def __init__(self):
        self.PacketIsClient = True
        self.PacketType = PacketTypeClient.TC_None
        self.content = ""

    def gen_msg(self):
        msg = b""
        if self.PacketIsClient:
            msg += b"\x01"
        else: msg += b"\x02"
        msg += chr(self.PacketType.value).encode("utf8")
        msg += self.content.encode("utf8")
        return msg

    def recieve(self, socket):
        recv= b""
        while len(recv) == 0: recv = socket.recv(2048)
        self.PacketIsClient = True if recv[0] == 1 else False
        self.PacketType = PacketTypeClient(recv[1]) if self.PacketIsClient else PacketTypeServer(recv[1])
        self.content = recv[2:].decode("utf8")

    def send(self, socket):
        socket.send(self.gen_msg())

    def __repr__(self):
        return f"<inetl.MPacket of inetl.{"PacketTypeClient" if self.PacketIsClient else "PacketTypeServer"}.{self.PacketType}: '{self.content}'>"

# string of packets
class SPacket(list): # inherits list for list of message packets
    def __init__(self, iscli: bool=True,total_content: str=""):
        for i in range(len(total_content)//2046):
            mpack = MPacket()
            mpack.PacketType = PacketTypeServer.TS_Elem if not iscli else PacketTypeClient.TC_Elem
            mpack.PacketIsClient = iscli
            self.append(mpack)
        self.iscli = iscli
        self.total_content = total_content

    def append(self, item:MPacket):
        list.append(self,item)

    def __eq__(self, total_content):
        list.clear(self)

    def __getitem__(self,index):
        return list.__getitem__(self,index)

    def __setitem__(self, index, item):
        list.__setitem__(self,index,item)

    def __len__(self):
        return list.__len__(self)

    def recieve(self, socket):
        list.clear(self)
        self.total_content = ""
        mpack = None
        end = False
        while not end:
            mpack = MPacket()
            mpack.recieve(socket)
            if mpack.PacketType in [PacketTypeClient.TC_End,PacketTypeServer.TS_End]:
                end = True
            elif mpack.PacketType in [PacketTypeClient.TC_Elem, PacketTypeServer.TS_Elem]:
                self.append(mpack)
                self.total_content += mpack.content

    def send(self,socket):
        for i in range(self.__len__()):
            mpack = self[i]
            print(mpack)
            mpack.send(socket)
        mpack = MPacket()
        mpack.PacketIsClient = self.iscli 
        mpack.PacketType = PacketTypeServer.TS_End if not self.iscli else PacketTypeClient.TC_End
        mpack.send(socket)