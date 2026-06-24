
#include <PacketDefs/packet.hpp>

std::string MPacket::ToString() {}

MPacket::MPacket() {}

std::vector<MPacket> SPacket::ToPacketList() {

    std::vector<MPacket> PacketList = {};

    MPacket Packet = MPacket();

    std::vector<std::string> Contents = {};

    int i = 0;
    while (i < this->PacketContent.size()) {
        Contents.insert(Contents.end(), this->PacketContent.substr(i, i + 1452))
        i += 1452;
    }

    Packet.CType = this->CType;
    Packet.SType = this->SType;
    strcpy(Packet.PacketContent, Contents[0].c_str());

    PacketList.insert(PacketList.end(), Packet);

    for (i = 0; i < Contents.size(); i++) {
        Packet = MPacket();
        Packet.CType = TC_Elem;
        Packet.SType = TS_Elem;
        if (i == Contents.size()-1) {
            Packet.CType = TC_End;
            Packet.SType = TS_End;
        }

        strcpy(Packet.PacketContent, Contents[0].c_str());
        PacketList.insert(PacketList.end(), Packet);
    }

    return PacketList;

}

SPacket::SPacket() {}

int SPacket::FromPacketList(std::vector<MPacket> PacketList) {
    if (PacketList.size() < 2) {
        return 0;
    }

    this->CType = PacketList[0].CType;
    this->SType = PacketList[0].SType;
    this->PacketContent = "";
    this->PacketContent += PacketList[0].PacketContent;

    for (unsigned int i = 1; i != PacketList.size(); i ++) {
        this->PacketContent += PacketList[i].PacketContent;
    }

    return 1;
}