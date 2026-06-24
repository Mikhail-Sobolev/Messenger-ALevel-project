
#ifndef __inc_packetdefs_packet
#define __inc_packetdefs_packet

    #include <PacketDefs/packetEnums.hpp>

    #include <string>
    #include <vector>

    class MPacket {
        public:
            PacketTypeClient CType;
            PacketTypeServer SType;
            char PacketContent[1452];
            
            MPacket();

            std::string ToString();
    };

    class SPacket {
        public:
            PacketTypeClient CType;
            PacketTypeServer SType;
            std::string PacketContent;

            SPacket ();

            int FromPacketList(std::vector<MPacket> PacketList);
            std::vector<MPacket> ToPacketList();
    };

#endif