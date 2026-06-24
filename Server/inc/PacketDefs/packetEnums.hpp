
#ifndef __inc_packetdefs_packetenums
#define __inc_packetdefs_packetenums

    typedef enum __packettypeclient {
        TC_None = 0,
        TC_LogIn = 1,
        TC_LogOut = 2,
        TC_ChangeDetails = 3,
        TC_ChatList = 4,
        TC_ServerList = 5,
        TC_MessageList = 6,
        TC_ChatDetail = 7,
        TC_ServerDetail = 8,
        TC_MessageDetail = 9,
        TC_SendMessage = 10,
        TC_Header = 11,
        TC_Elem = 12,
        TC_End = 13,
        TC_FriendList = 14,
        TC_AddFriend = 15,
        TC_UserDetail = 16,
        TC_CreateChat = 17,
        TC_CreateServer = 18,
        TC_ChangeServerDetail = 19
    } PacketTypeClient;

    typedef enum __packettypeserver {
        TS_None = 0,
        TS_CheckSuccess = 1,
        TS_CheckFail = 2,
        TS_Header = 3,
        TS_Elem = 4,
        TS_End = 5
    } PacketTypeServer;

#endif