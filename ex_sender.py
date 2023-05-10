import socket
import mss
import threading
import compress

# Set the screen resolution
WIDTH = 1920
HEIGHT = 1080

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
sock.bind(("0.0.0.0", 5000))

# Listen for connections
sock.listen(5)

# Accept a connection
conn, addr = sock.accept()

# Create a thread to send the screen to the receiver


def send_screen():
    # Create a screenshot object
    sct = mss()

    # Get the current screen
    img = sct.grab((0, 0, WIDTH, HEIGHT))

    # Compress the image
    pixels = compress(img.rgb, 6)

    # Send the size of the pixels
    size = len(pixels)
    size_len = (size.bit_length() + 7) // 8
    conn.send(bytes([size_len]))

    # Send the actual pixels
    size_bytes = size.to_bytes(size_len, 'big')
    conn.send(size_bytes)
    conn.sendall(pixels)


# Start the thread
thread = threading.Thread(target=send_screen)
thread.start()

# Print a message to the user
print("Screen sharing started.")

# Wait for the user to close the connection
while True:
    data = conn.recv(1024)
    if not data:
        break

# Close the connection
conn.close()

# Print a message to the user
print("Screen sharing stopped.")
