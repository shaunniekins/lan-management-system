import socket


def scan_network():
    """Scan the local network and return a list of available IP addresses"""
    ip_list = []
    subnet = '.'.join(socket.gethostbyname_ex(
        socket.gethostname())[2][0].split('.')[:3]) + '.'
    for i in range(1, 255):
        address = subnet + str(i)
        try:
            host = socket.gethostbyaddr(address)
            ip_list.append(address)
        except:
            pass
    return ip_list


# Example usage
print(scan_network())
