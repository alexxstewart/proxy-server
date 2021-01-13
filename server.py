import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(s)
    conn, addr = s.accept()
    print(conn)
    print(addr)
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if data:
                conn.sendall(data)
                print('data: ', data)
