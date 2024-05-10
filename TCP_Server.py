import socket
from socket import *
import os, threading, json, pyDes, random
from sympy import isprime
import time as time
from datetime import datetime, timedelta

tcp_port = 6001
current_time = datetime.now()
try:
    tcp_cli_sock = socket(AF_INET, SOCK_STREAM)
    hostname = input('Please enter your IP address: ')
    tcp_cli_sock.bind((hostname, tcp_port))
    # tcp_server_sock.listen(15)
except socket.error as err:
    print(f"An error occurred: {err}")
def receiver():
    while True:
        tcp_serv_sock = socket(AF_INET, SOCK_STREAM)
        hostname = input('Please enter your IP address: ')
        tcp_serv_sock.bind((hostname, tcp_port))
        received_data, received_address = tcp_serv_sock.recvfrom(2048)
        received_message = received_data.decode()
        received_msg_as_json = json.loads(received_message)
        ip_address = received_address[0]

        with open("contacts.json", "r") as ReadContactsInfo:
            contacts_data = json.load(ReadContactsInfo)
        for user in contacts_data['IP Address']:
            if user['IP Address'] == ip_address:
                recvd_uname = user['username']

        if('key' in received_msg_as_json):
            key = received_msg_as_json['key']
            print(f"{current_time} | Key received from {recvd_uname} at {ip_address}: Storing...")
            with open(f'key_{recvd_uname}.txt', 'w') as outfile:
                outfile.write(key)

        elif('encrypted_message' in received_msg_as_json):
            encrypted_message = received_msg_as_json['encrypted_message']
            print(f"{current_time} | Encrypted Message received from {recvd_uname} at {ip_address}: Decrypting...")

            decrypted_msg = pyDes.triple_des(key.ljust(24)).decrypt(encrypted_message, padmode=2)
            with open(f'chat_history_{recvd_uname}.txt', 'a') as outfile:
                outfile.write(f"{current_time} | {recvd_uname}: {decrypted_msg}\n")

        elif('unencrypted_message' in received_msg_as_json):
            unencrypted_message = received_msg_as_json['unencrypted_message']
            with open(f'chat_history_{recvd_uname}.txt', 'a') as outfile:
                outfile.append(f"{current_time} | {recvd_uname}: {unencrypted_message}\n")
        else:
            print("Awaiting...")