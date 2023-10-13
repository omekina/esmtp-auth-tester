import console
from base64 import b64encode
from pprint import PrettyPrinter
from ssl import create_default_context, SSLSocket
from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname


PORT = 465


def socket_lifetime(sock: SSLSocket, login: [str, str]) -> None:
    """ESMTP socket wrapper.

    Args:
        sock (SSLSocket): Established connection
        login ([str, str]): Username and password
    """
    
    # SSL/TLS certificate validation prompt
    print("==========CERT DUMP==============")
    prettyprinter = PrettyPrinter(indent=4)
    prettyprinter.pprint(sock.getpeercert())
    print("==========END CERT DUMP==========")
    trust = input("Trust (y/N)? ").lower() == "y"
    if not trust:
        print("Aborting")
        sock.close()
        return
    
    # HANDSHAKE
    response = sock.recv(4096).decode("utf-8", "ignore").split(" ", 2)
    console.print_stream("Connected", True)
    if len(response) < 3:
        console.print_event("Handshake failed", True)
        return
    console.print_stream("Server name: " + response[2], False)
    
    # Send hello
    my_hostname = gethostbyname(gethostname())
    sock.sendall(b'EHLO [' + my_hostname.encode("utf-8", "ignore") + b']\r\n')
    console.print_stream("Sent hello", True)
    response = sock.recv(4096).decode("utf-8", "ignore").lower()
    if not ("auth" in response and "login" in response):
        console.print_event("Authentication not supported", True)
        return
    console.print_stream("Got info", False)
    
    # Authentication - username
    sock.sendall(b'AUTH LOGIN\r\n')
    response = sock.recv(4096).decode("utf-8", "ignore")
    if response[:3] != "334" or response[4:16] != "VXNlcm5hbWU6":
        console.print_event("Server error", True)
        return
    sock.sendall(b64encode(login[0].encode("utf-8", "ignore")) + b'\r\n')
    console.print_stream("Sent username", True)
    
    # Authentication - password
    response = sock.recv(4096).decode("utf-8", "ignore")
    if response[:3] != "334" or response[4:16] != "UGFzc3dvcmQ6":
        console.print_event("Server error", True)
        return
    console.print_stream("Ok", False)
    sock.sendall(b64encode(login[1].encode("utf-8", "ignore")) + b'\r\n')
    console.print_stream("Sent password", True)
    response = sock.recv(4096).decode("utf-8", "ignore")
    if response[:3] != "235":
        console.print_event("Server error", True)
        return
    console.print_stream("Ok", False)
    
    # Console info
    console.print_event("Authentication done", False)


def run(hostname: str, login: [str, str]) -> None:
    """ESMTP protocol runner.

    Args:
        hostname (str): Target server hostname
        login ([str, str]): Username (e-mail) and password
    """
    
    # Creating SSL/TLS connection
    context = create_default_context()
    sock: socket = socket(AF_INET, SOCK_STREAM)
    ssock = context.wrap_socket(sock, server_hostname=hostname)
    ssock.connect((hostname, PORT))
    
    # Running socket logic
    try:
        socket_lifetime(ssock, login)
    except Exception as e:
        print(e)
    
    # Graceful exit
    try:
        ssock.sendall(b'QUIT')
    except: pass
    ssock.close()
