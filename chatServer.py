# Server half of the code, meant to connect and communicate with clients
# importing socket library to utilize sockets for communication
# Host to network (HTON, Network to Host)
# Wire Protocol idea for C: thread that accepts, thread per client
# Exit, how to shut down (Next thrusday 1600)
import socket # Utilize sockets for connections
import select # Specifically select.select()
import sys	# Alllow for breaks
from cryptography.fernet import Fernet # Encryption

# Create and write a key for encryption
def create_key():
	try:
		key = Fernet.generate_key()
		print(f"Your current key is: {key}")
        # Ben: Try to use a "with open():" statement whenever you are opening
        # and closing a file in the same function.
		file = open('Definitely_Not_the_Key', 'wb')
		file.write(key)
		file.close()
		return key
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

# Bind, Listen, Accept, Begin -- Change s name, and try except
def connect(saddr):
	try:
		# Initializing socket:
		# AF_INET refers to Internet Address Family, (specifically IPv4) allowing for outside connections
		# SOCK_STREAM refers to TCP Connection (DGRAM for UDP)
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Allow for reuse/reconnect of port
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(saddr)
		server_socket.listen()
		print("Successfully bound IP and Port")
		return server_socket
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

def client_left(exception_sockets, socket_list, client_names):
	try:
		# Remove exiting sockets
		for notified_socket in exception_sockets:
			socket_list.remove(notified_socket)
			del client_names[notified_socket]
		return exception_sockets, socket_list, client_names
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

# Receive client input
def receive_data(client_socket):
	try:
		# print("I am in receive_message")
		message_header = client_socket.recv(10)
		if len(message_header): # No user
			message_length = int(message_header.decode('utf-8').strip())
			return{"length": message_header, "data": client_socket.recv(message_length)}
		return False
	except Exception: # No user
		return False

# Accept and comminicate with clients -- No signle-nomatic variables
def run_server(server_socket, key):
	try:
		# initialize client socket lists
		socket_list = [server_socket]
		client_names = {}
		while True:
			# print("I am in run_server loop")
			# Accept/Post read sockets, and delete exception sockets (incoming and leaving)
			# select.select waits for 1 of three events: reads, writes, and exceptions
			# (we use read for incomming connections/messages, and exceptions for lost clients)
			read_sockets, write_sockets, exception_sockets = select.select(socket_list, [], socket_list, 1)
			# Go through sockets
			for notified_socket in read_sockets:
				# Socket is incoming client
				if notified_socket == server_socket:
					client_socket, client_address = server_socket.accept()
					# Receive the username
					user = receive_data(client_socket)
					# If no name, or error, skip
					if user: # Add user to the lists of clients
						socket_list.append(client_socket)
						client_names[client_socket] = user
						print(f"Accepted connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

				# Socket is client posting message
				else:
					'''
					a = client_socket.recv(1)
					if a != b'0':
						print("False message")
						print(a)
						continue
					'''
					message = receive_data(notified_socket)
					if message is False:
						print(f"Closed connection from {client_names[notified_socket]['data'].decode('utf-8')}")
						socket_list.remove(notified_socket)
						del client_names[notified_socket]
						continue
					user = client_names[notified_socket]
					print(f"Received message from {user['data'].decode('utf-8')}: {Fernet(key).decrypt(message['data']).decode('utf-8')}")
					# Post message to other clients
					for client_socket in client_names:
						if client_socket != notified_socket:
							client_socket.send(b'1' + user['length'] + message['length'] + user['data'] + message['data'])
			# Remove exiting clients
			exception_sockets, socket_list, client_names = client_left(exception_sockets, socket_list, client_names)
	except KeyboardInterrupt:
		print("Goodbye")
		sys.exit()
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

def main():
	# Ask for user input for server information, then try to connect
	# print("in main")
    # Ben: See my comment about input validation on chatClient.py
	server_socket = connect((input("Server IP: "), int(input("Server Port: "))))
	run_server(server_socket, create_key())
	# await asyncio.wait([run_server(server_socket, create_key()), await_inevitable()])

if __name__ == "__main__":
	# print("in _name_")
	print("Welcome to the Chat Server!\nIf you wish to exit at any time, use CTRL-C.\nFill out following to start:")
	main()
