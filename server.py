# import socket

import signal
import threading
import socket
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000      # Port to listen on (non-privileged ports are > 1023)

blacklist_domains = ['www.instagram.com', 'www.youtube.com']


class Server:
    def __init__(self):

        # Create a TCP socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Re-use the socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a public host, and a port
        self.serverSocket.bind((HOST, PORT))

        self.serverSocket.listen()  # become a server socket
        self.__clients = {}

        while True:
            print('------------------------------------')
            # Establish the connection
            (clientSocket, client_address) = self.serverSocket.accept()

            # d = threading.Thread(name=self._getClientName(client_address),target = self.proxy_thread, args = (clientSocket, client_address))
            # d.setDaemon(True)
            # d.start()
            data = clientSocket.recv(4096)
            print('data to send: ', data)
            data_string = str(data, 'utf-8')
            # parse the first line
            first_line = data_string.split('\n')[0]

            # get url
            url = first_line.split(' ')[1]
            print('url: ', url)

            http_pos = url.find("://")  # find pos of ://
            if (http_pos == -1):
                temp = url
            else:
                temp = url[(http_pos+3):]  # get the rest of url

            port_pos = temp.find(":")  # find the port pos (if any)

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

            print('web server: ', webserver)

            # check if website has been blacklisted
            for i in range(0, len(blacklist_domains)):
                if blacklist_domains[i] in url:
                    print('url blacklisted')
                    clientSocket.close()
                    break

            safe_url = url.find('googlevideo')
            print(safe_url)
            if url.find('googlevideo') == -1:
                serverToSend = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                serverToSend.settimeout(100000)
                serverToSend.connect((webserver, port))
                serverToSend.sendall(data)

                while 1:
                    # receive data from web server
                    dataFromServer = serverToSend.recv(100000000)
                    print('received data from server: ', dataFromServer)

                    if (len(dataFromServer) > 0):
                        # send to browser/client
                        self.serverSocket.sendall(data)
                    else:
                        break


server = Server()
