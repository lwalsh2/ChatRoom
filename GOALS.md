## C Goals
    - Get the C side working like the python, where the user can enter text and see other people's messages.
    - Make it so multiple people can be connected at the same time.
    - Display the IP and port of new connections
    - Add command line parameters for IP and port to listen on

## Python Goals
    - Make it so that messages keep coming in while the user is typing.
    - Add command line parameters for IP and port to listen on
        - Note: If no parameter is provided, you can either print an error or prompt just like you are doing.
        - Example: python3 chatServer.py --ip 0.0.0.0 --port 1234
    - Add a command line parameter to retrieve messages and exit
        - Example: python3 chatClient.py --ip 127.0.0.1 --port 1234 --retrieve
        - Example: python3 chatClient.py -a 127.0.0.1 -p 1234 -r
    - Add a command line parameter to send a message and exit
        - Example: python3 chatClient.p --ip 127.0.0.1 -p 1234 --message "Hello world!"

## General Goals
    - Make sure the C server works with the python client and vice versa.

## Bonus Points
    - Keep a history of messages and send them to new clients who connect
    - Use asyncio in the python version
    - Use pthreads in the C version
