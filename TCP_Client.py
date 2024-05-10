import socket
from socket import *
import os, threading, json, pyDes, random
from sympy import isprime
import time as time
from datetime import datetime, timedelta

current_time = datetime.now()
tcp_port = 6001
tcp_cli_sock = socket(AF_INET, SOCK_STREAM)

def save_own_msg_to_history(target_destination, own_username, own_plaintext_msg):
    with open(f'chat_history_{target_destination}.txt', 'a', encoding='utf-8') as AppendChatHistoryFile:
        AppendChatHistoryFile.write(f"{current_time} | {own_username}: {own_plaintext_msg}\n")

def begin_announcer():
    print(f"Note that the received messages will be shown in the TCP Server. This is the client.\n"
          "The session is ready! Awaiting your messages...\n")
def chat_initiator():
    print("Welcome to the TCP Client!\nThis program is used for displaying available users, sending messages to them, or viewing chat history logs.\n"
          "Fetching your username from the 'own_user_info.json' file...\nIf you want to change your username, just delete the 'own_user_info.json' file.\n")
    handler()

def handler():
    if os.path.exists("own_user_info.json"):
        with open("own_user_info.json", "r") as ReadOwnUserInfo:
            own_data = json.load(ReadOwnUserInfo)
            own_username = own_data['username']
            print(f"Welcome back, {own_username}!\n")
    else:
        print("Seems like you didn't start the UDP client and server before.\n"
              "Please start them first, for registration and user detection purposes.\nTerminating...")
        exit()

    while True:
        choice = input("Please choose an action (users/chat/history): ").lower()
        with open("contacts.json", "r") as ReadContactsInfo:
            contacts_data = json.load(ReadContactsInfo)

        if choice == 'users':
            users = contacts_data['users']
            print("All users (Activity within the last 15 minutes)")
            for user in users:
                last_seen_time = datetime.strptime(user['Last Seen'], "%d/%m/%Y %H:%M:%S")
                if (current_time - last_seen_time) < timedelta(minutes=15):
                    username = user['username']
                    status = user['Status']
                    print(f"{username} ({status})\n")
        elif choice == 'chat':
            while True:
                target_destination = input("Who do you want to chat with?: ")
                for user in contacts_data['users']:
                    last_seen_time = datetime.strptime(user['Last Seen'], "%d/%m/%Y %H:%M:%S")
                    if target_destination.lower() == user['username'].lower() and (
                            (current_time - last_seen_time) < timedelta(minutes=15)):
                        target_ip = user['IP Address']
                        tcp_cli_sock.connect((target_ip, tcp_port))
                    else:
                        print(f"The user you've specified is either offline, or that username has never existed.")
                        exit()

                security = input("Please specify your chat security preference (secure/unsecure): ").lower()
                if security == 'unsecure':
                    print(f"Initiating plaintext unsecure chat, with {target_destination} at {target_ip}...\n")
                    begin_announcer()
                    while True:
                        own_plaintext_msg = input(f"{own_username}: ")
                        save_own_msg_to_history(target_destination, own_username, own_plaintext_msg)
                        plaintext_msg_as_json = {'unencrypted_message': own_plaintext_msg}
                        tcp_cli_sock.sendto(json.dumps(plaintext_msg_as_json).encode(), (target_ip, tcp_port))
                        print(f"{current_time} | Plaintext message sent to {target_destination} at {target_ip}.\n")

                elif security == 'secure':
                    print(f"Initiating secure chat, with {target_destination} at {target_ip}...\n")
                    tcp_cli_sock.sendto()
                    begin_announcer()
                    own_plaintext_msg = input(f"{own_username}: ")
                    save_own_msg_to_history(target_destination, own_username, own_plaintext_msg)
                    own_encrypted_msg = pyDes.triple_des
                    encrypted_msg_as_json = {'encrypted_message': own_encrypted_msg}
                    tcp_cli_sock.sendto(json.dumps(encrypted_msg_as_json).encode(), (target_ip, tcp_port))
                    print(f"{current_time} | Encrypted message sent to {target_destination} at {target_ip}.\n")

                else:
                    print("Invalid input: Please specify 'secure' or 'unsecure' only.")
        elif choice == 'history':
            view_history = input("Which logs? (username): ")
            if(os.path.exists(f"chat_history_{view_history}.txt")):
                with open(f"chat_history_{view_history}.txt", 'r', encoding='utf-8') as ReadChatHistoryFile:
                    content = ReadChatHistoryFile.read()
            else:
                print("The specified user could not be found.")
        else:
            print("Invalid input!\n")

chat_initiator()