from socket import *
import time, json
udpCliSock = socket(AF_INET, SOCK_DGRAM)  # opening a new UDP Socket

def service_announcer():
    print("Welcome to the UDP Client!"
          "\n----------------------\n"
          "To announce your presence to other users in the network, this client will be utilized.\n"
          "\n----------------------\n")

    username = input("Please enter your username to continue:")
    username_as_json = {"username":username}
    with open('own_user_info.json', 'w') as LocalUserInfo:
        LocalUserInfo.write(json.dumps(username_as_json))

    broadcast_addr = input("Now, enter the broadcast address of the network you're connected here: ")
    print("Broadcasting your username across the network...\n"
          "Unless you close this client, it will keep getting broadcast every 8 seconds.")
    server_address = (broadcast_addr, 6000)
    while True:
        message = json.dumps(username_as_json).encode('utf-8')
        udpCliSock.sendto(message, server_address)
        time.sleep(8)

service_announcer()