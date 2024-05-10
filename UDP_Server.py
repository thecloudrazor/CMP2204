from socket import *
import os, threading, json
import time as time
from datetime import datetime, timedelta



def load_user_data():
      with open('contacts.json', 'w') as CreatingFile:
            json.dump({"users": []}, CreatingFile)
      with open('contacts.json', 'r') as OnlineUsers:
            return json.load(OnlineUsers)

def save_user_data(online_user_data):
      with open('contacts.json', 'w') as ModifyingFile:
            json.dump(online_user_data, ModifyingFile, indent=4, sort_keys=True)

def listener(udp_socket, last_ping_time, online_user_data):
      while True:
            received_data, received_address = udp_socket.recvfrom(2048)
            received_message = received_data.decode('utf-8')
            received_msg_as_json = json.loads(received_message)
            new_user = received_msg_as_json['username']
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            ip_address = received_address[0]
            last_ping_time[new_user] = datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S")

            if(new_user not in [user['username'] for user in online_user_data['users']]):
                  new_entry = {"username": new_user, "IP Address": received_address[0], "Last Seen": timestamp, "Status": "Online"}
                  online_user_data['users'].append(new_entry)
                  save_user_data(online_user_data)
                  print(f"New user found! | Username: {new_user} | IP: {ip_address} | Timestamp: {timestamp}")
            else:
                  for user in online_user_data['users']:
                        if user['username'] == new_user:
                              if (user['Status'] == 'Away'):
                                    print(f"User {user['username']} is online again, and no longer away.")
                              user['Status'] = "Online"
                              user['Last Seen'] = timestamp
                              save_user_data(online_user_data)
                              break

def user_status_checker(last_ping_time, online_user_data):
      while True:
            current_time = datetime.now()
            for user in online_user_data['users']:
                  if (current_time - last_ping_time.get(user['username'], current_time)).total_seconds() > 10:
                        user['Status'] = 'Away'
            save_user_data(online_user_data)
            time.sleep(1)

def peer_discovery():
      print("Welcome to the UDP Server!\nThis is used for listing active users in the network.\n---------------------\n"
            "Receiving status probes from other users...\n---------------------\n")

      serverPort = 6000  # the UDP server's port. This will receive peer announcements
      try:
            udpServSock = socket(AF_INET, SOCK_DGRAM)
            udpServSock.bind(('', serverPort))
            # udpServSock.listen(15)
            print("Socket successfully created.\n")
      except socket.error as err:
            print(f"An error occured: {err}")


      last_ping_time = {}
      online_user_data = load_user_data()

      listener_thread = threading.Thread(target=listener, args=(udpServSock,last_ping_time, online_user_data))
      status_checker_thread = threading.Thread(target=user_status_checker, args=(last_ping_time, online_user_data))

      listener_thread.start()
      status_checker_thread.start()

      listener_thread.join()
      status_checker_thread.join()

peer_discovery()