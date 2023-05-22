import socket
from zlib import decompress
import pygame
import tkinter as tk


root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()


def recvall(conn, length):
    """ Retrieve all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host, port):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
    clock = pygame.time.Clock()
    watching = True

    sock = socket.socket()
    sock.connect((host, port))
    try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break

            # Retrieve the size of the pixels length, the pixels length, and pixels
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            pixels = decompress(recvall(sock, size))

            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

            # Display the picture
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    finally:
        sock.close()


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    main(ip_address, 9997)
