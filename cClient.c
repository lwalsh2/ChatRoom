#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

// Socket builder method

/* Ben:
 * (This message is duplicated in cServer.c)
 * Here you are returning a "struct sockaddr_in", this
 * is called an 'aggregate return' and it's frowned upon.
 * It is safest to return only values that fit in one register
 * like ints, pointers, floats, and char's (not structs).
 *
 * The two most common fixes here are to:
 *  - Add a pointer parameter to a struct
 *  - Return a pointer to a newly malloc'd struct
 * 
 * Try both of them out.
 */ 
struct sockaddr_in create_struct(int port){
	struct sockaddr_in server_struct;
	server_struct.sin_family = AF_INET; // IPv4
	server_struct.sin_addr.s_addr = INADDR_ANY; // shortcut for self
    // Ben: ^ This is not a shortcut for self. You wanted INADDR_LOOPBACK,
    // here is a stack overflow link with good information on using INADDR_ANY.
    // https://stackoverflow.com/questions/16508685/understanding-inaddr-any-for-socket-programming/16510000
	server_struct.sin_port = htons( port );
	return server_struct;
}


int main() {
	// Socket Creation
	// IPv4 (AF_INET), TCP (SOCK_STREAM),  Internet Protocol, TCP->0->default
    // Ben: Make sure you check that this worked! The man page for socket will tell you
    // about how this call could fail and what will be returned if it does.
	int client_socket = socket(AF_INET, SOCK_STREAM, 0);

	// Create socket address struct
	struct sockaddr_in server_struct = create_struct(1234);

	// Connect to the server
    /* Ben:
     * This call could also fail, then we are calling recv right after and not checking
     * that value either (recv will always fail if we call it on a socket that failed to connect).
     * That means the message will just show up as blank, with no way to distinguish it from
     * actually receiving a blank message.
     */
	connect(client_socket, (struct sockaddr *)&server_struct, sizeof(server_struct));

	// Receive from server
	char message[256] = "";
    /* Ben:
     * Another thing to consider with recv on a TCP socket is that the whole message is not
     * guaranteed to arrive all at once. You could send("hello there") and only recv "hel",
     * then recv again and get "lo there". One solution is to send the length of the
     * message first, then keep reading until you get the whole message.
     */
	int wasRecv = recv(client_socket, message, sizeof(message), 0);
	printf("%s", message);

	printf("\nFinished\n");

	return 0;
}
