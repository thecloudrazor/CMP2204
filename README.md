# CMP2204
Introduction to Computer Networks -- Term Project
# P2P Chat Application

This is a simple P2P chat application written in Python. It allows users to chat with each other in a secure or unsecure way. 

## Prerequisites

- Python 3.x
- pyDes library

## Usage

1. After downloading, navigate to the project directory.

2. Install the required Python libraries using "pip install (library name goes here)"

3. First, run the UDP Server for receiving announcements from other users and saving their info into your local contacts.json file:
python UDP_Server.py

4. Then, run the UDP Client for announcing yourself over the network:
python UDP_Client.py

5. In seperate terminals, run the TCP apps (Server first, client second):
python TCP_Server.py
python TCP_Client.py

### Client Options

- **List Users**: Lists all users who have been active within the last 15 minutes.
- **Chat**: Allows you to chat with another user. You will be asked to specify the username of the user you want to chat with and your chat security preference (secure/unsecure).
- **History**: Allows you to view the chat history with a specific user.