import _thread
import socket
import sys

# AUTHOR: Alex Stewart

# GLOBAL VARS
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

blacklist_domains = ['www.instagram.com', 'www.youtube.com']

# Class server handles proxy functionality


class Server:
    def __init__(self):
        # Create a TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Re-use the socket
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a public host, and a port
        self.server_socket.bind((HOST, PORT))

        self.server_socket.listen(20)  # allow up to 20 client connections

    def handle_request(self, client_socket, client_address):
        client_socket.setblocking(True)

        data = client_socket.recv(4096)

        # convert the byte data to string to extract the url info
        data_string = str(data, 'utf-8')

        # parse the first line
        first_line = data_string.split('\n')[0]

        # get url
        url = first_line.split(' ')[1]

        http_pos = url.find("://")  # find pos of ://
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]  # get the rest of url

        port_pos = temp.find(":")  # get the position of the port

        # find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):
            # default port
            port = 80
            webserver = temp[:webserver_pos]

        else:  # specific port
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        # create the server to send the client data to
        serverToSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverToSend.settimeout(5)  # set the timeout to 5 seconds
        serverToSend.connect((webserver, port))
        serverToSend.sendall(data)  # send all the data

        print('url: ', url)
        print('webserver: ', webserver)

        while 1:
            # receive data from web server
            print('WAITING ON DATA FROM: ', url)
            dataFromServer = serverToSend.recv(1024)

            if (len(dataFromServer) > 0):
                # send to browser/client
                print('received data from server: ', dataFromServer)
                client_socket.send(dataFromServer)
            else:
                break

    def start(self):

        # set up a loop which creates a new thread for each request
        while True:
            # create the new thread and pass in the handle request function as well as socket and address
            _thread.start_new_thread(
                self.handle_request, self.server_socket.accept())


server = Server()

if __name__ == '__main__':
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        # stop the server
        print("Ctrl C - Stopping server")

        # close the socket
        server.server_socket.close()
        sys.exit(1)
