
import socket
import enum

@enum.Enum
class PacketTypeClient:
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

@enum.Enum
class PacketTypeServer:
    TS_None = 0
    TS_CheckSuccess = 1
    TS_CheckFail = 2
    TS_Elem = 3
    TS_End = 4

class MPacket:
    pass

class SPacket:
    pass

class Server:
    pass