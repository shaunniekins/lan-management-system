import socket
import zlib
import pygame
import threading


# Set the screen resolution
WIDTH = 1920
HEIGHT = 1080

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the sender
sock.connect(("localhost", 5000))

# Create a pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a thread to receive the screen from the sender


def receive_screen():
    # Create a buffer
    buf = bytearray()

    # Keep receiving data until we get the size of the pixels
    while True:
        data = sock.recv(1024)
        if not data:
            break
        buf.extend(data)

    # Get the size of the pixels
    size = int.from_bytes(buf, "big")

    # Create a buffer for the pixels
    pixels = bytearray(size)

    # Keep receiving data until we have all the pixels
    while len(pixels) < size:
        data = sock.recv(1024)
        if not data:
            break
        pixels.extend(data)

    # Decompress the pixels
    decompressed_pixels = zlib.decompress(pixels)

    # Create an image from the pixels
    img = pygame.image.frombuffer(decompressed_pixels, (WIDTH, HEIGHT), "RGB")

    # Draw the image to the screen
    screen.blit(img, (0, 0))

    # Update the screen
    pygame.display.update()


# Start the thread
thread = threading.Thread(target=receive_screen)
thread.start()

# Run the pygame event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

# Close the socket
sock.close()

# Quit pygame
pygame.quit()
