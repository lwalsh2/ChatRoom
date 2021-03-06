#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

// Socket builder method
struct sockaddr_in create_struct(int port){
	struct sockaddr_in server_struct;
	server_struct.sin_family = AF_INET; // IPv4
	server_struct.sin_addr.s_addr = INADDR_ANY; // shortcut for self
	server_struct.sin_port = htons( port );
	return server_struct;
}


int main() {
	// Socket Creation
	// IPv4 (AF_INET), TCP (SOCK_STREAM),  Internet Protocol, TCP->0->default
	printf("Creating Socket\n");
	int server_socket = socket(AF_INET, SOCK_STREAM, 0);

	// System call that allows for reuse of IP address and port
	printf("Overriding previous bind\n");
	int option_value = 1;
	setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &option_value, sizeof(option_value));
	// int setsockopt(int socket, int level, int option_name, const void *option_value, socklen_t option_len);

	// Create socket address struct
	printf("Creating Struct\n");
	struct sockaddr_in server_struct = create_struct(1234);
	int struct_length = sizeof(server_struct);

	// Bind the socket to IP address and Port
	printf("Binding socket\n");
	bind(server_socket, (struct sockaddr *)&server_struct, struct_length);

	// Turns socket into a listener (listens for connections, and backlogs up to 5)
	printf("Listening for Clients\n");

	// Declare variables for incoming clients
	int client_socket;
	// Loop Listen-Accept-Send commands. Can be CTRL-C'd out
	while(1) {
		// Listen for incoming clients (backhaul of 5)
		listen(server_socket, 5);
		// Accept incoming client (Was the cause of earlier issue)
		if ((client_socket = accept(server_socket, (struct sockaddr *)&server_struct, (socklen_t*)&struct_length))<0)
    {
			printf("Failed to accept\n");
			break;
		}
		printf("Received a client: %d\n", client_socket);

		// Send message to CLient
		char message[256] = "This is the message - Server";
		send(client_socket, message, sizeof(message) , 0);
	}
  return 0;
}
