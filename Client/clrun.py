#!/usr/bin/python3

import inetabst.inetl as inetl
from enum import Enum, auto
import socket
import random
import pygame
import pygame.font as font
pygame.init()
font.init()

sys_font = font.SysFont("iosevka",30)
window = pygame.display.set_mode((640,480))

end = False

message_text = ""
message_send = False
msg_disable = False

current_chatroom_id = 0
current_server_id = 0

target_port = "127.0.0.1"
target_addr = 65432

# inheretence from enum class
class Page(Enum):
    login_prompt = auto()
    failure = auto()
    main_page = auto()
    friends_list = auto()
    server_list = auto()
    chatroom_list = auto()

    send_friend_invite = auto()
    invite_list = auto()

    friend_page = auto()
    server_page = auto()
    chatroom_page = auto()

cur_page = Page.login_prompt
err_msg = ""
err_back_page = Page.login_prompt

part_selected = 0
username = ""
password = ""

sock = None

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((target_port,target_addr))

def button_login():
    global cur_page, sock, err_msg,err_back_page

    # dynamic object instance
    pack = inetl.MPacket()
    pack.PacketType = inetl.PacketTypeClient.TC_LogIn
    pack.content += username + "\x00" + password
    pack.send(sock)
    
    pack.recieve(sock)

    if pack.PacketType == inetl.PacketTypeServer.TS_CheckSuccess:
        cur_page = Page.main_page
    else:
        cur_page = Page.failure
        err_msg = pack.content
        err_back_page = Page.login_prompt

    
    #main_page = True

def logout():
    global end, sock
    pack = inetl.MPacket()
    pack.PacketType = inetl.PacketTypeClient.TC_LogOut
    pack.send(sock)
    end = True    


# should be an array containing dictionaries which describe the button.
buttons = []

def process_key(key):
    global message_text,message_send,part_selected

    if key.key == pygame.K_DOWN:
        part_selected += 1
    elif key.key == pygame.K_UP:
        part_selected -= 1
    
    try: chr(key.key)
    
    except:
        return 0
    
    if  message_send == False:
        if chr(key.key).isalnum():
            message_text += chr(key.key)
        if chr(key.key) in "\n\r":
            message_send = True
        if chr(key.key) == "\b":
            message_text = message_text[:-1]



list_of_stuff = []

while not end:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
            break
        elif event.type == pygame.KEYDOWN:
            process_key(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                b_render = sys_font.render(button["text"], True, (240,240,240), (100,100,100))
                b_rect = b_render.get_rect()
                b_rect.center = button["centre"]
                if b_rect.collidepoint(event.pos):
                    button["func"]()

    window.fill((10,10,10))
    if cur_page == Page.login_prompt:
        msg_disable = False

        buttons = [{"text": "login", "func": button_login, "centre": (100,100)}]

        part_selected = part_selected % 2 # only two parts to login (username and password)

        if message_send:

            if part_selected == 0:
                username = message_text
            else:
                password = message_text

            message_send = False
            message_text = ""

        pswd_render = None
        user_render = None
        if part_selected == 0:
            user_render = sys_font.render(" Username: " + username, True, (240,240,240), (70,70,70))
            pswd_render = sys_font.render(" Password: " + "".join(["*" for x in range(len(password))]), True, (200,200,200), (50,50,50))
        else:
            user_render = sys_font.render(" Username: " + username, True, (200,200,200), (50,50,50))
            pswd_render = sys_font.render(" Password: " + "".join(["*" for x in range(len(password))]), True, (240,240,240), (70,70,70))
        pswd_rect = pswd_render.get_rect()
        user_rect = user_render.get_rect()
        pswd_rect.center = (300,200)
        user_rect.center = (300,100)

        window.blit(pswd_render,pswd_rect)
        window.blit(user_render,user_rect)
    elif cur_page == Page.failure:
        msg_disable = True
        buttons = [{"text":err_msg,"func": lambda : globals().update(cur_page = globals()["err_back_page"]),"centre":(320,240)}]
        pass
    elif cur_page == Page.main_page:
        msg_disable = True
        buttons = [{"text":"to friends list","func":lambda : globals().update(cur_page = Page.friends_list), "centre": (320,240) },
                   {"text":"to server list","func":lambda : globals().update(cur_page = Page.server_list), "centre": (320,140) },
                   {"text":"to chatroom list","func":lambda : globals().update(cur_page = Page.chatroom_list), "centre": (320,340)},
                   {"text":"logout","func": logout, "centre":(320,440)}]
    elif cur_page in (Page.friends_list,Page.server_list,Page.chatroom_list):
        msg_disable = True
        buttons = [{"text":"back to menu","func":lambda : (globals().update(cur_page = Page.main_page), globals().update(list_of_stuff = [])), "centre": (100,70) }]
        buttons += [{"text":"send invite ","func":lambda:0,"centre":(100,110)},{"text":"invites     ","func":lambda:0,"centre":(100,150)}]        
        if list_of_stuff == []:
            if cur_page == Page.friends_list:
                c_pack = inetl.MPacket()
                c_pack.PacketType = inetl.PacketTypeClient.TC_FriendList
                c_pack.send(sock)
                s_pack = inetl.SPacket()
                s_pack.recieve(sock)
                for i in range(len(s_pack)):
                    list_of_stuff += [[s_pack[i].content, lambda: 0]]
            elif cur_page == Page.chatroom_list:
                c_pack = inetl.MPacket()
                c_pack.PacketType = inetl.PacketTypeClient.TC_ChatList
                c_pack.send(sock)
                s_pack = inetl.SPacket()
                s_pack.recieve(sock)
                for i in range(len(s_pack)):
                    list_of_stuff += [[s_pack[i].content, lambda: 0]]
            elif cur_page == Page.server_list:
                c_pack = inetl.MPacket()
                c_pack.PacketType = inetl.PacketTypeClient.TC_ServerList
                c_pack.send(sock)
                s_pack = inetl.SPacket()
                s_pack.recieve(sock)
                for i in range(len(s_pack)):
                    list_of_stuff += [[s_pack[i].content, lambda: 0]]

        c_loc = 0
        for button in list_of_stuff:
            buttons += [{"text":button[0],"func":button[1],"centre":(320,150+(c_loc*40))}]
            c_loc += 1
    else:
        print("Error: unknown/invalid state")
        end = True

    for b in buttons:
        b_render = sys_font.render(b["text"], True, (240,240,240), (100,100,100))
        b_rect = b_render.get_rect()
        b_rect.center = b["centre"]
        window.blit(b_render,b_rect)


    top_details = sys_font.render(f"@{username}>>[{cur_page}]", True, (100,100,100),(10,10,10))
    top_det_rect = top_details.get_rect()
    top_det_rect.center = (320,30)
    window.blit(top_details,top_det_rect)
    
    if not msg_disable:
        cur_render = sys_font.render(f" >> " + message_text, True, (240,240,240), (10,10,10))
        cur_rect = cur_render.get_rect()
        cur_rect.center=(300,440)
        window.blit(cur_render,cur_rect)
    else:
        message_send = False
        message_text = ""
    pygame.display.update()

sock.close() 
font.quit()
pygame.quit()
quit(0)