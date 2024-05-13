import socket
import threading
import json
import pyDes
import base64
import datetime

# Diffie-Hellman parameters
g = 5
n = 23

def read_contacts_data():
    with open("contacts.json", "r") as ReadContactsInfo:
        return json.load(ReadContactsInfo)

def pad_or_truncate_key(key):
    # If key is less than 8 bytes, pad it with zeros
    if len(key) < 8:
        key += b'0' * (8 - len(key))
    # If key is more than 8 bytes, truncate it
    elif len(key) > 8:
        key = key[:8]
    return key

def save_received_msg_to_history(sender_username, received_msg):
    with open(f'chat_history_{sender_username}.txt', 'a', encoding='utf-8') as AppendChatHistoryFile:
        AppendChatHistoryFile.write(f"RECEIVED | {datetime.datetime.now()} | {sender_username}: {received_msg}\n")

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        if not request:
            break  # Client has disconnected
        data = json.loads(request.decode())
        sender_username = [user['username'] for user in read_contacts_data()['users'] if user['IP Address'] == client_socket.getpeername()[0]][0]

        if 'key' in data:
            # Generate Diffie-Hellman key
            client_key = int(data['key'])
            print(f"Received client's key: {client_key}")
            server_key = (g ** n) % n
            print(f"Generated server key: {server_key}")
            shared_key = (client_key ** n) % n
            print(f"Generated shared key: {shared_key}")
            shared_key = str(shared_key).encode()  # Convert to bytes
            shared_key = pad_or_truncate_key(shared_key)  # Pad or truncate to 8 bytes
            print(f"Final key after padding or truncating: {shared_key.decode('utf-8')}")

            # Send server key to client
            response = json.dumps({'key': server_key})
            client_socket.send(response.encode())
            print("Sent server key to client.")

        elif 'encrypted_message' in data:
            # Decrypt message using pyDes
            encrypted_message = base64.b64decode(data['encrypted_message'])  # Decode from base64
            des = pyDes.des(shared_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
            decrypted_message = des.decrypt(encrypted_message)
            decrypted_message = decrypted_message.decode()  # Convert bytes to string
            print(f"{datetime.datetime.now()} | {sender_username}: Decrypted message: {decrypted_message}")
            save_received_msg_to_history(sender_username, decrypted_message)

        elif 'unencrypted_message' in data:
            # Directly print the message
            print(f"{datetime.datetime.now()} | {sender_username} says: {data['unencrypted_message']}")
            save_received_msg_to_history(sender_username, data['unencrypted_message'])

        else:
            print("Unknown data received.")

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.70', 6001))
    server_socket.listen(5)

    print("Listening on port 6001...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")

        # Handle clients in separate threads
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    server()