# Client half of the code, meant to connect and communicate with server
# importing socket library to utilize sockets for communication
import socket # Utilize sockets for connections
import errno  # Error handling
import sys	# Alllow for breaks
from datetime import datetime # Timestamps for messages (haven't made Zulu yet)
from cryptography.fernet import Fernet # Encryption

# Grab key for encryption
def read_key():
	try:
        # Ben: You should probably take a parameter for the keyfile
        #  instead of or in addition to looking for it locally.
		# Open the file the Server made with thee key
		file = open('Definitely_Not_the_Key', 'rb')
		print("Successfully retreived key")
		return file.read()
	except Exception as error_message:
        # Ben: Instead of casting a wide net, try to except the exact
        # situations that arise and deal with them appropriately. For example,
        # if you get a FileNotFoundError you can tell the user how to generate
        # a key.
		print('General error', str(error_message))
		sys.exit()

# Connect to the server
def connect(saddr):
	try:
		# Initializing socket:
		# AF_INET refers to Internet Address Family, allowing for outside connections
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Reaching out to the server for a connection
		client_socket.connect(saddr)
		print("Successfully Connected!")
		# Allows for recv to work unhindered
		client_socket.setblocking(False)
		return client_socket
	except Exception as error_message:
        # Ben: I wont comment all of them, but take what I said about exceptions
        # above and apply it to every 'except Exception'
		print('General error', str(error_message))
		sys.exit()

# Create and send username to server
def username(client_socket):
	try:
		# Create a name for yourself within the server
		username = input("Username: ")
		# Encode username for server to read
		encoded_username = username.encode('utf-8')
		# Header protocol
		username_length = f"{len(encoded_username):<{10}}".encode('utf-8')
		# Sending username to server to track (0 for add user, 1 for send message)
        # Ben: Just like with C, send (and recv) in python isn't guaranteed to send all
        # of the bytes in one go, it should be in a loop (or use the sendall function)
		client_socket.send(username_length + encoded_username)
		# print(f"Protocol Sent: {username_length + encoded_username}")
		return username
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

# Proceed to chat with server
def chat(client_socket, name, key):
	# Initial Message in chat
	print("You are in the chat server. Use !quit to exit, enter to send/refresh messages")
	# Looping Messages/Messaging
	try:
		while True:
			# Enter message to send to chat (enter to refresh chat log)
			message = input(f"{name} > ")
			# Provide a quit function
			if message == "!quit":
				print("Leaving Chat. Goodbye!")
				sys.exit()
			# Returns true if a message was typed. Otherwise refreshes
			if message:
				# Adding timestamp for recordkeeping
				message = str(datetime.now()).split('.')[0] + " : " + message
				# Encode for transport
				message = message.encode('utf-8')
				# Encrypt for security
				message = Fernet(key).encrypt(message)
				message_length = f"{len(message) :< {10}}".encode('utf-8')
				client_socket.send(message_length + message)
				# print(f"Protocol Sent: {message_length + message}")
			# Receiving Messages (expected IOerrors)
			try:
				while True:
					# Receive messages
                    # Ben: Why are you sending junk?
					junk = client_socket.recv(1)
					username_length = client_socket.recv(10)
					if not len(username_length):
						print("Connection closed by server")
						sys.exit()
					message_length = int(client_socket.recv(10).decode('utf-8').strip())
                    # Ben: I know I've commented about it many times but if you only receive 5 bytes here,
                    # the other 5 bytes of message length will end up in the username length instead,
                    # probably causing your client to freeze as it waits for "0000500000" bytes.
                    #   Also, try out sending bytes as an integer instead of a string. You're using 10
                    # bytes to convey a number between 0 and 9,999,999,999 when you can convey a number
                    # between 0 and 4,294,967,295 (2**32 - 1) with just 4 bytes using an integer
					username = client_socket.recv(int(username_length.decode('utf-8').strip())).decode('utf-8')
					# Decode to readable string
					message = Fernet(key).decrypt(client_socket.recv(message_length)).decode('utf-8')
					print(f"{username} > {message}")
			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
					print('Reading error', str(e))
					sys.exit()
				continue
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

def main():
	# Ask for user input for server information, then try to connect
    # Ben: Make sure you test nonsense inputs like "Apple Pie" for a server address and
    # display a meaningful error message like "That isn't a valid IP." or "That port number
    # is out of range."
	client_socket = connect((input("Server IP: "), int(input("Server Port: "))))
	name = username(client_socket)
	chat(client_socket, name, read_key())


if __name__ == "__main__":
	main()
